"""Out-of-process llama.cpp chat/embedding engine.

Supervises a ``llama-server`` subprocess and proxies OpenAI-compatible requests
to it. Everything that touches the outside world — process spawning and HTTP —
is injected, so tests never spawn a real process or open a socket:

* ``spawn(argv) -> proc`` defaults to :class:`subprocess.Popen`.
* ``http_get(url) -> resp`` and ``http_post(url, json=..., stream=...) -> resp``
  default to thin ``requests`` wrappers, imported lazily.

The proxied response objects follow the ``requests`` contract used here:
``resp.status_code``, ``resp.json()`` and ``resp.iter_lines()``.
"""

from __future__ import annotations

import json
import os
from typing import Any, Callable, Iterator, List, Optional

from .base import Engine, EngineState


def _default_spawn(argv: List[str]) -> Any:
    """Default process spawner: :class:`subprocess.Popen` (imported lazily)."""
    import subprocess  # noqa: PLC0415

    return subprocess.Popen(argv)


def _default_http_get(url: str) -> Any:
    """Default GET using ``requests`` (imported lazily)."""
    import requests  # noqa: PLC0415

    return requests.get(url, timeout=5)


def _default_http_post(url: str, *, json: Optional[dict] = None, stream: bool = False) -> Any:
    """Default POST using ``requests`` (imported lazily)."""
    import requests  # noqa: PLC0415

    return requests.post(url, json=json, stream=stream, timeout=300)


class LlamaCppEngine(Engine):
    """Chat/embedding engine backed by a ``llama-server`` subprocess.

    Args:
        model_path: Path to the GGUF model file.
        model_id: Reported model id (forwarded to the server payloads).
        host: Bind host for the server.
        port: Bind port for the server.
        binary_path: Path to the ``llama-server`` executable.
        n_ctx: Context window size (``-c``).
        n_threads: Worker threads (``-t``); defaults to CPU count.
        mmproj_path: Optional multimodal projector; enables the vision capability.
        extra_args: Extra CLI flags appended verbatim.
        spawn: Injectable process spawner (defaults to ``subprocess.Popen``).
        http_get: Injectable GET callable for health checks.
        http_post: Injectable POST callable for chat/embedding proxying.
    """

    def __init__(
        self,
        model_path: str,
        model_id: str,
        *,
        host: str = "127.0.0.1",
        port: int = 8080,
        binary_path: str = "llama-server",
        n_ctx: int = 4096,
        n_threads: Optional[int] = None,
        mmproj_path: Optional[str] = None,
        extra_args: Optional[List[str]] = None,
        spawn: Optional[Callable[[List[str]], Any]] = None,
        http_get: Optional[Callable[[str], Any]] = None,
        http_post: Optional[Callable[..., Any]] = None,
    ) -> None:
        self.model_path = model_path
        self.model_id = model_id
        self.host = host
        self.port = port
        self.binary_path = binary_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.mmproj_path = mmproj_path
        self.extra_args = list(extra_args or [])
        self._spawn = spawn or _default_spawn
        self._http_get = http_get or _default_http_get
        self._http_post = http_post or _default_http_post
        self._proc: Optional[Any] = None
        self.state = EngineState.STOPPED

    @property
    def base_url(self) -> str:
        """Base URL of the supervised server."""
        return f"http://{self.host}:{self.port}"

    def _build_argv(self) -> List[str]:
        """Assemble the ``llama-server`` command line."""
        threads = self.n_threads if self.n_threads is not None else (os.cpu_count() or 4)
        argv = [
            self.binary_path,
            "--host", self.host,
            "--port", str(self.port),
            "-m", self.model_path,
            "-c", str(self.n_ctx),
            "-t", str(threads),
        ]
        if self.mmproj_path:
            argv += ["--mmproj", self.mmproj_path]
        argv += self.extra_args
        return argv

    def start(self) -> None:
        """Spawn the ``llama-server`` subprocess."""
        self.state = EngineState.STARTING
        try:
            self._proc = self._spawn(self._build_argv())
            self.state = EngineState.READY
        except Exception:
            self.state = EngineState.CRASHED
            self._proc = None
            raise

    def stop(self) -> None:
        """Terminate the subprocess (falling back to kill)."""
        proc = self._proc
        if proc is not None:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                kill = getattr(proc, "kill", None)
                if callable(kill):
                    kill()
        self._proc = None
        self.state = EngineState.STOPPED

    def health(self) -> bool:
        """Return ``True`` when ``GET /health`` responds with HTTP 200."""
        try:
            resp = self._http_get(f"{self.base_url}/health")
        except Exception:
            return False
        return getattr(resp, "status_code", None) == 200

    def chat(self, messages: List[dict], **opts: object) -> Iterator[str]:
        """Proxy a streaming chat completion, yielding text deltas."""
        payload: dict = {"model": self.model_id, "messages": messages, "stream": True}
        payload.update(opts)
        resp = self._http_post(
            f"{self.base_url}/v1/chat/completions", json=payload, stream=True
        )
        raise_for_status = getattr(resp, "raise_for_status", None)
        if callable(raise_for_status):
            raise_for_status()

        for raw_line in resp.iter_lines():
            if not raw_line:
                continue
            line = raw_line.decode("utf-8") if isinstance(raw_line, (bytes, bytearray)) else raw_line
            line = line.strip()
            if not line.startswith("data:"):
                continue
            data = line[len("data:"):].strip()
            if data == "[DONE]":
                break
            try:
                obj = json.loads(data)
            except json.JSONDecodeError:
                continue
            for choice in obj.get("choices", []):
                text = choice.get("delta", {}).get("content")
                if text:
                    yield text

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Proxy an embeddings request to ``/v1/embeddings``."""
        payload = {"model": self.model_id, "input": texts}
        resp = self._http_post(
            f"{self.base_url}/v1/embeddings", json=payload, stream=False
        )
        raise_for_status = getattr(resp, "raise_for_status", None)
        if callable(raise_for_status):
            raise_for_status()
        body = resp.json()
        return [item["embedding"] for item in body.get("data", [])]

    @property
    def capabilities(self) -> frozenset:
        """Text + embeddings, plus vision when an mmproj path is configured."""
        caps = {"text", "embeddings"}
        if self.mmproj_path:
            caps.add("vision")
        return frozenset(caps)
