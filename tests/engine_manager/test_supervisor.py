"""Tests for EngineSupervisor: crash recovery, hot-swap and the RAM governor."""

from __future__ import annotations

from typing import Optional

from litertlm.engines.base import EngineState
from litertlm.engines.supervisor import EngineSupervisor


class FakeEngine:
    """Minimal engine double with call counters and scripted health values."""

    def __init__(self, health_sequence: Optional[list[bool]] = None, default_health: bool = True) -> None:
        self.state = EngineState.STOPPED
        self.start_calls = 0
        self.stop_calls = 0
        self._health_seq = list(health_sequence) if health_sequence is not None else None
        self._default_health = default_health

    def start(self) -> None:
        self.start_calls += 1
        self.state = EngineState.READY

    def stop(self) -> None:
        self.stop_calls += 1
        self.state = EngineState.STOPPED

    def health(self) -> bool:
        if self._health_seq:
            return self._health_seq.pop(0)
        return self._default_health


class FakeClock:
    """Injectable monotonic clock advanced explicitly by tests."""

    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


# -- crash recovery --------------------------------------------------------


def test_ensure_healthy_restarts_on_crash() -> None:
    engine = FakeEngine(health_sequence=[False, True])
    sup = EngineSupervisor(tier="full", chat_engine=engine)

    assert sup.ensure_healthy(engine) is True
    assert engine.stop_calls == 1
    assert engine.start_calls == 1


def test_ensure_healthy_bounded_retries() -> None:
    engine = FakeEngine(default_health=False)
    sup = EngineSupervisor(tier="full", chat_engine=engine, max_restarts=3)

    assert sup.ensure_healthy(engine) is False
    assert engine.start_calls == 3
    assert engine.stop_calls == 3


def test_ensure_healthy_noop_when_healthy() -> None:
    engine = FakeEngine(default_health=True)
    sup = EngineSupervisor(tier="full", chat_engine=engine)

    assert sup.ensure_healthy(engine) is True
    assert engine.start_calls == 0
    assert engine.stop_calls == 0


def test_check_health_restarts_chat_engine() -> None:
    engine = FakeEngine(health_sequence=[False, True])
    sup = EngineSupervisor(tier="full", chat_engine=engine)

    report = sup.check_health()
    assert report == {"chat": True}
    assert engine.start_calls == 1


# -- hot-swap --------------------------------------------------------------


def test_swap_chat_engine_stops_old_starts_new() -> None:
    old = FakeEngine()
    new = FakeEngine()
    sup = EngineSupervisor(tier="full", chat_engine=old)

    result = sup.swap_chat_engine(new)

    assert result is new
    assert sup.chat_engine is new
    assert old.stop_calls == 1
    assert new.start_calls == 1


# -- RAM governor ----------------------------------------------------------


def test_lite_tier_idle_unloads_and_reloads_asr() -> None:
    clock = FakeClock()
    created: list[FakeEngine] = []

    def asr_factory() -> FakeEngine:
        engine = FakeEngine()
        created.append(engine)
        return engine

    sup = EngineSupervisor(
        tier="lite",
        asr_engine_factory=asr_factory,
        clock=clock,
        idle_timeout=100.0,
    )

    e1 = sup.get_asr_engine()
    assert e1 is created[0]
    assert e1.start_calls == 1

    # Not yet idle — nothing unloaded.
    clock.advance(50)
    assert sup.collect_idle() == []
    assert e1.stop_calls == 0

    # Past the idle timeout — ASR is unloaded.
    clock.advance(60)  # total elapsed = 110 >= 100
    assert sup.collect_idle() == ["asr"]
    assert e1.stop_calls == 1

    # Reload on demand builds a fresh engine.
    e2 = sup.get_asr_engine()
    assert e2 is created[1]
    assert e2 is not e1
    assert e2.start_calls == 1


def test_full_tier_keeps_aux_engines_resident() -> None:
    clock = FakeClock()

    def emb_factory() -> FakeEngine:
        return FakeEngine()

    sup = EngineSupervisor(
        tier="full",
        embedding_engine_factory=emb_factory,
        clock=clock,
        idle_timeout=1.0,
    )

    engine = sup.get_embedding_engine()
    clock.advance(10_000)
    assert sup.collect_idle() == []
    assert engine.stop_calls == 0


def test_unconfigured_aux_engines_return_none() -> None:
    sup = EngineSupervisor(tier="lite", chat_engine=FakeEngine())
    assert sup.get_asr_engine() is None
    assert sup.get_embedding_engine() is None


def test_get_chat_engine_starts_lazily() -> None:
    engine = FakeEngine()
    sup = EngineSupervisor(tier="lite", chat_engine=engine)

    returned = sup.get_chat_engine()
    assert returned is engine
    assert engine.start_calls == 1
    assert engine.state == EngineState.READY
