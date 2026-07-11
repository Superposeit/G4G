"""In-process LiteRT-LM chat engine.

Wraps the ``litert_lm`` runtime that previously lived inline in ``bridge.py``.
LiteRT-LM allows only a single conversation session at a time, so all
generation is serialised behind a per-engine lock (the original ``_request_lock``
behaviour). The ``litert_lm`` import is deferred to :meth:`start` so this module
stays importable — and the engine stays unit-testable — without the library.
"""

from __future__ import annotations

import os
import threading
from typing import Any, Iterator, List, Optional

from .base import Engine, EngineState


def _extract_text(content: Any) -> str:
    """Extract plain text from an OpenAI-style message ``content`` value."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "".join(parts)
    return str(content)


def _split_messages(messages: List[dict]) -> tuple[list[dict], str]:
    """Split OpenAI messages into LiteRT history + the final user message.

    Mirrors the original bridge behaviour: every message except the last is
    flattened to ``{"role", "content"}`` text history, and the last message's
    text becomes the prompt.
    """
    history: list[dict] = []
    for m in messages[:-1]:
        history.append({"role": m.get("role", "user"), "content": _extract_text(m.get("content", ""))})
    last = messages[-1].get("content", "") if messages else ""
    return history, _extract_text(last)


class LiteRTEngine(Engine):
    """Text-only chat engine backed by the in-process LiteRT-LM runtime.

    Args:
        model_path: Path to the ``.litertlm`` model file.
        model_id: Reported model id.
        litert_module: Optional pre-imported ``litert_lm`` module. When ``None``
            (the default) it is imported lazily inside :meth:`start`; tests inject
            a fake here so no real library or model is needed.
    """

    def __init__(
        self,
        model_path: str,
        model_id: str,
        *,
        litert_module: Optional[Any] = None,
    ) -> None:
        self.model_path = model_path
        self.model_id = model_id
        self._litert = litert_module
        self._engine: Optional[Any] = None
        # Serialises sessions — LiteRT rejects a second concurrent conversation.
        self._request_lock = threading.Lock()
        self.state = EngineState.STOPPED

    def start(self) -> None:
        """Load the model, importing ``litert_lm`` lazily if not injected."""
        self.state = EngineState.STARTING
        try:
            if self._litert is None:
                import litert_lm  # noqa: PLC0415 — deferred so import stays optional

                self._litert = litert_lm

            if not os.path.exists(self.model_path):
                raise FileNotFoundError(
                    f"Model file not found at {self.model_path}. "
                    "Run 'python scripts/download_litertlm_model.py' to download it."
                )

            # Text-only: vision/audio backends are disabled in litert-lm-nightly.
            self._engine = self._litert.Engine(self.model_path)
            self.state = EngineState.READY
        except Exception:
            self.state = EngineState.CRASHED
            self._engine = None
            raise

    def stop(self) -> None:
        """Drop the in-process engine reference."""
        self._engine = None
        self.state = EngineState.STOPPED

    def health(self) -> bool:
        """Return ``True`` when the model is loaded and ready."""
        return self.state == EngineState.READY and self._engine is not None

    def chat(self, messages: List[dict], **opts: object) -> Iterator[str]:
        """Stream a text completion, yielding decoded text chunks.

        Generation is serialised behind ``_request_lock`` to satisfy LiteRT's
        single-session constraint.
        """
        if self._engine is None:
            raise RuntimeError("LiteRTEngine.chat called before start()")

        history, user_message = _split_messages(messages)

        with self._request_lock:
            with self._engine.create_conversation(messages=history) as conversation:
                for chunk in conversation.send_message_async(user_message):
                    text = ""
                    for item in chunk.get("content", []):
                        if item.get("type") == "text":
                            text += item.get("text", "")
                    if text:
                        yield text

    @property
    def capabilities(self) -> frozenset:
        """LiteRT bridge is text-only in the current library version."""
        return frozenset({"text"})
