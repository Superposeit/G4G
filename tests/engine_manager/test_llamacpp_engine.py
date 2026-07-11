"""Tests for LlamaCppEngine with all process/HTTP interaction injected."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from litertlm.engines.base import EngineState
from litertlm.engines.llamacpp_engine import LlamaCppEngine


class FakeStreamResp:
    """Fake streaming HTTP response exposing the ``requests`` contract used."""

    def __init__(self, lines: list) -> None:
        self._lines = lines

    def iter_lines(self):
        return iter(self._lines)

    def raise_for_status(self) -> None:
        pass


# -- start / spawn flags ---------------------------------------------------


def test_start_spawns_with_expected_flags() -> None:
    captured: dict = {}

    def spawn(argv):
        captured["argv"] = argv
        return SimpleNamespace(terminate=lambda: None, wait=lambda timeout=None: 0)

    engine = LlamaCppEngine(
        "model.gguf",
        "gemma-4-E2B-it",
        host="1.2.3.4",
        port=9090,
        binary_path="/opt/llama-server",
        n_ctx=2048,
        n_threads=6,
        spawn=spawn,
    )
    engine.start()

    argv = captured["argv"]
    assert argv[0] == "/opt/llama-server"
    assert argv[argv.index("--host") + 1] == "1.2.3.4"
    assert argv[argv.index("--port") + 1] == "9090"
    assert argv[argv.index("-m") + 1] == "model.gguf"
    assert argv[argv.index("-c") + 1] == "2048"
    assert argv[argv.index("-t") + 1] == "6"
    assert "--mmproj" not in argv
    assert engine.state == EngineState.READY


def test_mmproj_enables_vision_capability_and_flag() -> None:
    captured: dict = {}

    def spawn(argv):
        captured["argv"] = argv
        return SimpleNamespace(terminate=lambda: None, wait=lambda timeout=None: 0)

    engine = LlamaCppEngine(
        "model.gguf",
        "gemma",
        mmproj_path="mmproj.gguf",
        spawn=spawn,
    )
    engine.start()

    assert captured["argv"][captured["argv"].index("--mmproj") + 1] == "mmproj.gguf"
    assert "vision" in engine.capabilities
    assert {"text", "embeddings"} <= engine.capabilities


def test_capabilities_without_mmproj() -> None:
    engine = LlamaCppEngine("m.gguf", "g")
    assert engine.capabilities == frozenset({"text", "embeddings"})


# -- health ----------------------------------------------------------------


def test_health_maps_status_code() -> None:
    ok = LlamaCppEngine("m", "g", http_get=lambda url: SimpleNamespace(status_code=200))
    assert ok.health() is True

    bad = LlamaCppEngine("m", "g", http_get=lambda url: SimpleNamespace(status_code=503))
    assert bad.health() is False


def test_health_false_on_connection_error() -> None:
    def raiser(url):
        raise ConnectionError("server down")

    engine = LlamaCppEngine("m", "g", http_get=raiser)
    assert engine.health() is False


# -- stop ------------------------------------------------------------------


def test_stop_terminates_process() -> None:
    proc = MagicMock()
    proc.wait.return_value = 0
    engine = LlamaCppEngine("m", "g", spawn=lambda argv: proc)
    engine.start()

    engine.stop()

    proc.terminate.assert_called_once()
    assert engine.state == EngineState.STOPPED
    assert engine._proc is None


# -- chat streaming --------------------------------------------------------


def test_chat_yields_proxied_chunks() -> None:
    lines = [
        b'data: {"choices":[{"delta":{"content":"Hello"}}]}',
        b"",
        b'data: {"choices":[{"delta":{"content":" world"}}]}',
        b"data: [DONE]",
    ]
    captured: dict = {}

    def http_post(url, json=None, stream=False):
        captured["url"] = url
        captured["json"] = json
        captured["stream"] = stream
        return FakeStreamResp(lines)

    engine = LlamaCppEngine("m", "gemma-4-E2B-it", http_post=http_post)
    out = list(engine.chat([{"role": "user", "content": "hi"}], temperature=0.5))

    assert out == ["Hello", " world"]
    assert captured["url"].endswith("/v1/chat/completions")
    assert captured["json"]["messages"] == [{"role": "user", "content": "hi"}]
    assert captured["json"]["stream"] is True
    assert captured["json"]["temperature"] == 0.5


# -- embeddings ------------------------------------------------------------


def test_embed_proxies_to_server() -> None:
    def http_post(url, json=None, stream=False):
        assert url.endswith("/v1/embeddings")
        assert json["input"] == ["a", "b"]
        return SimpleNamespace(
            json=lambda: {"data": [{"embedding": [0.1, 0.2]}, {"embedding": [0.3, 0.4]}]},
            raise_for_status=lambda: None,
        )

    engine = LlamaCppEngine("m", "g", http_post=http_post)
    assert engine.embed(["a", "b"]) == [[0.1, 0.2], [0.3, 0.4]]
