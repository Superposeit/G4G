"""Hardware-tier recommendation.

Pure, I/O-free logic that maps a machine's RAM (and platform/architecture) onto
a concrete :class:`TierPlan` describing which engine and models to run. Being
side-effect free, it is fully table-testable.

The ladder (see the project brief):

* RAM >= 8 GB  -> "full"   engine "llamacpp", GGUF gemma-4-E2B-it Q4_K_M,
                            vision on,  ASR whisper-small
* 4 <= RAM < 8 -> "lite"   engine "litert", litertlm gemma-4-E2B-it,
                            vision off, ASR whisper-base
* RAM < 4 GB   -> "client" engine None (recommend LAN client mode),
                            no local chat model, ASR whisper-tiny

Special case: Windows on ARM64 has no ``litert-lm`` wheels, so any tier that
would otherwise pick "litert" is forced onto "llamacpp"/GGUF instead, keeping
the tier assignment (chosen purely by RAM) unchanged.
"""

from __future__ import annotations

import platform
from dataclasses import dataclass
from typing import Optional

_CHAT_MODEL = "gemma-4-E2B-it"
_GGUF_QUANT = "Q4_K_M"
_ARM_MACHINES = frozenset({"arm64", "aarch64"})


@dataclass(frozen=True)
class TierPlan:
    """Concrete engine/model plan for a hardware tier.

    Attributes:
        tier: One of ``"full"``, ``"lite"`` or ``"client"``.
        engine: ``"llamacpp"``, ``"litert"`` or ``None`` (client mode).
        chat_model: Chat model id, or ``None`` when no local chat model runs.
        quant: GGUF quantisation label, or ``None`` for non-GGUF formats.
        format: ``"gguf"``, ``"litertlm"`` or ``None``.
        enable_vision: Whether the multimodal vision path should be enabled.
        asr_model: Whisper model size to pair with this tier.
        reason: Human-readable justification for the recommendation.
    """

    tier: str
    engine: Optional[str]
    chat_model: Optional[str]
    quant: Optional[str]
    format: Optional[str]
    enable_vision: bool
    asr_model: str
    reason: str


def _is_windows_arm(system: str, machine: str) -> bool:
    """Return ``True`` for the Windows-on-ARM64 special case."""
    return system.lower().startswith("win") and machine.lower() in _ARM_MACHINES


def recommend(
    hardware: object,
    *,
    platform_system: Optional[str] = None,
    machine: Optional[str] = None,
) -> TierPlan:
    """Recommend an engine/model plan for the given hardware.

    Args:
        hardware: Duck-typed object exposing ``ram_total_gb`` and, ideally,
            ``platform`` / ``architecture`` (matches ``HardwareSpecs``).
        platform_system: Override for the OS name. Falls back to
            ``hardware.platform`` then :func:`platform.system`.
        machine: Override for the CPU architecture. Falls back to
            ``hardware.architecture`` then :func:`platform.machine`.

    Returns:
        A fully-populated :class:`TierPlan`.
    """
    ram = float(getattr(hardware, "ram_total_gb", 0.0) or 0.0)

    system = platform_system if platform_system is not None else getattr(hardware, "platform", None)
    if not system:
        system = platform.system()
    arch = machine if machine is not None else getattr(hardware, "architecture", None)
    if not arch:
        arch = platform.machine()

    win_arm = _is_windows_arm(system, arch)

    if ram >= 8.0:
        # "full" always runs llama.cpp/GGUF; Windows-on-ARM already lands here.
        reason = f"RAM {ram:.1f} GB >= 8 GB: full tier on llama.cpp (GGUF)."
        if win_arm:
            reason += " Windows/ARM64 uses GGUF (no litert-lm wheels)."
        return TierPlan(
            tier="full",
            engine="llamacpp",
            chat_model=_CHAT_MODEL,
            quant=_GGUF_QUANT,
            format="gguf",
            enable_vision=True,
            asr_model="whisper-small",
            reason=reason,
        )

    if ram >= 4.0:
        if win_arm:
            return TierPlan(
                tier="lite",
                engine="llamacpp",
                chat_model=_CHAT_MODEL,
                quant=_GGUF_QUANT,
                format="gguf",
                enable_vision=False,
                asr_model="whisper-base",
                reason=(
                    f"RAM {ram:.1f} GB in [4, 8) GB: lite tier. Windows/ARM64 "
                    "has no litert-lm wheels, so llama.cpp (GGUF) is used."
                ),
            )
        return TierPlan(
            tier="lite",
            engine="litert",
            chat_model=_CHAT_MODEL,
            quant=None,
            format="litertlm",
            enable_vision=False,
            asr_model="whisper-base",
            reason=f"RAM {ram:.1f} GB in [4, 8) GB: lite tier on LiteRT-LM.",
        )

    return TierPlan(
        tier="client",
        engine=None,
        chat_model=None,
        quant=None,
        format=None,
        enable_vision=False,
        asr_model="whisper-tiny",
        reason=(
            f"RAM {ram:.1f} GB < 4 GB: client tier — run no local chat model, "
            "recommend LAN client mode against a nearby full/lite node."
        ),
    )
