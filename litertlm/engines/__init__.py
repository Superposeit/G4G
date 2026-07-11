"""Dual-engine "Engine Manager" for the LiteRT-LM bridge.

Exposes the engine abstraction and its concrete implementations behind one
OpenAI-compatible service. Every submodule is import-safe without ``litert_lm``,
``requests`` or any engine binary — heavy dependencies are imported lazily at
engine ``start()`` time — so this package can be imported during test collection.
"""

from __future__ import annotations

from .base import Engine, EngineState
from .llamacpp_engine import LlamaCppEngine
from .litert_engine import LiteRTEngine
from .supervisor import EngineSupervisor
from .tiers import TierPlan, recommend

__all__ = [
    "Engine",
    "EngineState",
    "LiteRTEngine",
    "LlamaCppEngine",
    "EngineSupervisor",
    "TierPlan",
    "recommend",
]
