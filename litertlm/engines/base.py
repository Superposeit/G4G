"""Engine abstraction for the dual-engine Engine Manager.

Defines the :class:`Engine` abstract base class implemented by both the
in-process LiteRT-LM engine and the out-of-process llama.cpp engine, plus the
:class:`EngineState` lifecycle enum shared by supervisors and health checks.

Nothing in this module imports ``litert_lm``, ``requests`` or any engine binary
so it is safe to import anywhere, including test collection.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterator, List


class EngineState(str, Enum):
    """Lifecycle state of an :class:`Engine`.

    Inherits from ``str`` so the value serialises cleanly in JSON responses and
    compares equal to its plain-string form.
    """

    STOPPED = "stopped"
    STARTING = "starting"
    READY = "ready"
    CRASHED = "crashed"


class Engine(ABC):
    """Common interface for an inference engine.

    Concrete engines wrap either an in-process runtime (LiteRT-LM) or a
    supervised subprocess (llama.cpp ``llama-server``). All lifecycle methods
    are synchronous; the FastAPI bridge drives them from a streaming generator.
    """

    #: Current lifecycle state. Subclasses update this as they start/stop/crash.
    state: EngineState = EngineState.STOPPED

    @abstractmethod
    def start(self) -> None:
        """Bring the engine up (load model / spawn subprocess).

        Implementations should defer heavy imports (e.g. ``litert_lm``) until
        this call so the module stays importable without them.
        """

    @abstractmethod
    def stop(self) -> None:
        """Tear the engine down and release its resources."""

    @abstractmethod
    def health(self) -> bool:
        """Return ``True`` when the engine is ready to serve requests."""

    @abstractmethod
    def chat(self, messages: List[dict], **opts: object) -> Iterator[str]:
        """Stream a chat completion, yielding decoded text chunks.

        Args:
            messages: OpenAI-style message dicts (``role``/``content``).
            **opts: Optional generation parameters (temperature, max_tokens…).

        Yields:
            Incremental text fragments of the assistant reply.
        """

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Return one embedding vector per input text.

        Raises:
            NotImplementedError: if the engine has no embedding capability.
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not support embeddings"
        )

    def transcribe(self, audio: bytes, **opts: object) -> str:
        """Transcribe audio bytes to text.

        Raises:
            NotImplementedError: if the engine has no audio capability.
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not support audio transcription"
        )

    @property
    @abstractmethod
    def capabilities(self) -> frozenset:
        """Set of supported modalities from ``{text, vision, audio, embeddings}``."""
