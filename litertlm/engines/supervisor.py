"""Engine supervisor: lifecycle, crash-recovery and the RAM governor.

The :class:`EngineSupervisor` owns the active chat engine plus optional,
lazily-created ASR and embedding engines. It is the single object the FastAPI
bridge talks to. Responsibilities:

* start/stop the managed engines;
* health-check with bounded restart-on-crash;
* hot-swap the chat model (stop old, start new);
* the RAM governor — on the ``"lite"`` tier auxiliary engines (ASR/embedding)
  are loaded on demand and unloaded after an idle timeout, while on ``"full"``
  they stay resident.

Time is injected via a ``clock`` callable so idle-unload is testable without
real sleeping.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

from .base import Engine, EngineState

# Tiers on which auxiliary engines are kept resident rather than idle-unloaded.
_RESIDENT_TIERS = frozenset({"full"})


@dataclass
class _Slot:
    """A lazily-instantiated auxiliary engine plus its bookkeeping."""

    factory: Callable[[], Engine]
    resident: bool
    engine: Optional[Engine] = None
    last_used: float = 0.0


@dataclass
class EngineSupervisor:
    """Owns and supervises the active chat/ASR/embedding engines.

    Args:
        tier: Hardware tier (``"full"``/``"lite"``/``"client"``) — drives the
            RAM governor's resident-vs-on-demand policy for auxiliary engines.
        chat_engine: The chat engine (kept resident once started).
        asr_engine_factory: Zero-arg factory building a fresh ASR engine.
        embedding_engine_factory: Zero-arg factory building an embedding engine.
        clock: Monotonic time source (defaults to :func:`time.monotonic`).
        idle_timeout: Seconds of inactivity before an on-demand auxiliary engine
            is unloaded.
        max_restarts: Bounded restart attempts for :meth:`ensure_healthy`.
    """

    tier: str = "full"
    chat_engine: Optional[Engine] = None
    asr_engine_factory: Optional[Callable[[], Engine]] = None
    embedding_engine_factory: Optional[Callable[[], Engine]] = None
    clock: Callable[[], float] = None  # type: ignore[assignment]
    idle_timeout: float = 300.0
    max_restarts: int = 3

    _asr: Optional[_Slot] = field(default=None, init=False, repr=False)
    _embed: Optional[_Slot] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.clock is None:
            import time  # noqa: PLC0415

            self.clock = time.monotonic
        resident = self.tier in _RESIDENT_TIERS
        if self.asr_engine_factory is not None:
            self._asr = _Slot(factory=self.asr_engine_factory, resident=resident)
        if self.embedding_engine_factory is not None:
            self._embed = _Slot(factory=self.embedding_engine_factory, resident=resident)

    # -- lifecycle ---------------------------------------------------------

    def start(self) -> None:
        """Start the chat engine (auxiliaries start lazily on first use)."""
        if self.chat_engine is not None and self.chat_engine.state != EngineState.READY:
            self.chat_engine.start()

    def stop(self) -> None:
        """Stop every managed engine and drop auxiliary instances."""
        if self.chat_engine is not None:
            self.chat_engine.stop()
        for slot in (self._asr, self._embed):
            if slot and slot.engine is not None:
                slot.engine.stop()
                slot.engine = None

    # -- chat --------------------------------------------------------------

    def get_chat_engine(self, *, ensure_started: bool = True) -> Optional[Engine]:
        """Return the chat engine, starting it on first use if requested."""
        engine = self.chat_engine
        if engine is not None and ensure_started and engine.state != EngineState.READY:
            engine.start()
        return engine

    def swap_chat_engine(self, new_engine: Engine, *, start: bool = True) -> Engine:
        """Hot-swap the chat model: stop the old engine, install and start new.

        Returns:
            The newly-installed engine.
        """
        old = self.chat_engine
        if old is not None:
            old.stop()
        self.chat_engine = new_engine
        if start:
            new_engine.start()
        return new_engine

    # -- auxiliary engines (RAM governor) ---------------------------------

    def _acquire(self, slot: Optional[_Slot]) -> Optional[Engine]:
        """Instantiate+start ``slot``'s engine on demand and stamp last-used."""
        if slot is None:
            return None
        if slot.engine is None:
            slot.engine = slot.factory()
            slot.engine.start()
        slot.last_used = self.clock()
        return slot.engine

    def get_asr_engine(self) -> Optional[Engine]:
        """Return the ASR engine, loading it on demand (``None`` if unconfigured)."""
        return self._acquire(self._asr)

    def get_embedding_engine(self) -> Optional[Engine]:
        """Return the embedding engine, loading on demand (``None`` if unconfigured)."""
        return self._acquire(self._embed)

    def collect_idle(self) -> list[str]:
        """Unload non-resident auxiliary engines idle past ``idle_timeout``.

        Returns:
            Names (``"asr"``/``"embedding"``) of the engines that were unloaded.
        """
        now = self.clock()
        unloaded: list[str] = []
        for name, slot in (("asr", self._asr), ("embedding", self._embed)):
            if slot is None or slot.resident or slot.engine is None:
                continue
            if now - slot.last_used >= self.idle_timeout:
                slot.engine.stop()
                slot.engine = None
                unloaded.append(name)
        return unloaded

    # -- health / crash recovery ------------------------------------------

    def ensure_healthy(self, engine: Optional[Engine]) -> bool:
        """Restart ``engine`` (up to ``max_restarts``) until it is healthy.

        Returns:
            ``True`` if the engine is healthy (possibly after a restart),
            ``False`` if it stayed unhealthy after all attempts.
        """
        if engine is None:
            return False
        if engine.health():
            return True
        for _ in range(self.max_restarts):
            engine.stop()
            engine.start()
            if engine.health():
                return True
        return False

    def check_health(self) -> dict:
        """Health-check every resident engine, restarting crashed ones.

        Returns:
            Mapping of engine name to its post-check health boolean. Only
            currently-loaded engines are reported.
        """
        report: dict[str, bool] = {}
        if self.chat_engine is not None:
            report["chat"] = self.ensure_healthy(self.chat_engine)
        for name, slot in (("asr", self._asr), ("embedding", self._embed)):
            if slot and slot.engine is not None:
                report[name] = self.ensure_healthy(slot.engine)
        return report
