"""Table-driven tests for the hardware-tier recommendation ladder."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from litertlm.engines.tiers import TierPlan, recommend


def _hw(ram: float, platform: str = "Linux", arch: str = "x86_64") -> SimpleNamespace:
    """Build a duck-typed HardwareSpecs-like stub."""
    return SimpleNamespace(ram_total_gb=ram, platform=platform, architecture=arch)


# (id, hardware kwargs, expected field values — every non-reason field asserted)
_CASES = [
    (
        "8gb-full",
        dict(ram=8.0),
        dict(
            tier="full",
            engine="llamacpp",
            chat_model="gemma-4-E2B-it",
            quant="Q4_K_M",
            format="gguf",
            enable_vision=True,
            asr_model="whisper-small",
        ),
    ),
    (
        "16gb-full",
        dict(ram=16.0),
        dict(
            tier="full",
            engine="llamacpp",
            chat_model="gemma-4-E2B-it",
            quant="Q4_K_M",
            format="gguf",
            enable_vision=True,
            asr_model="whisper-small",
        ),
    ),
    (
        "6gb-lite-litert",
        dict(ram=6.0),
        dict(
            tier="lite",
            engine="litert",
            chat_model="gemma-4-E2B-it",
            quant=None,
            format="litertlm",
            enable_vision=False,
            asr_model="whisper-base",
        ),
    ),
    (
        "3gb-client",
        dict(ram=3.0),
        dict(
            tier="client",
            engine=None,
            chat_model=None,
            quant=None,
            format=None,
            enable_vision=False,
            asr_model="whisper-tiny",
        ),
    ),
    (
        "win-arm64-6gb-llamacpp",
        dict(ram=6.0, platform="Windows", arch="arm64"),
        dict(
            tier="lite",
            engine="llamacpp",
            chat_model="gemma-4-E2B-it",
            quant="Q4_K_M",
            format="gguf",
            enable_vision=False,
            asr_model="whisper-base",
        ),
    ),
    (
        "boundary-8.0-full",
        dict(ram=8.0),
        dict(
            tier="full",
            engine="llamacpp",
            chat_model="gemma-4-E2B-it",
            quant="Q4_K_M",
            format="gguf",
            enable_vision=True,
            asr_model="whisper-small",
        ),
    ),
    (
        "boundary-4.0-lite",
        dict(ram=4.0),
        dict(
            tier="lite",
            engine="litert",
            chat_model="gemma-4-E2B-it",
            quant=None,
            format="litertlm",
            enable_vision=False,
            asr_model="whisper-base",
        ),
    ),
]


@pytest.mark.parametrize("case_id,hw_kwargs,expected", _CASES, ids=[c[0] for c in _CASES])
def test_recommend_ladder(case_id: str, hw_kwargs: dict, expected: dict) -> None:
    plan = recommend(_hw(**hw_kwargs))

    assert isinstance(plan, TierPlan)
    for field, value in expected.items():
        assert getattr(plan, field) == value, f"{case_id}: {field}"
    # reason is always a non-empty human-readable string
    assert isinstance(plan.reason, str) and plan.reason


def test_boundary_just_below_8_is_lite() -> None:
    assert recommend(_hw(7.99)).tier == "lite"


def test_boundary_just_below_4_is_client() -> None:
    assert recommend(_hw(3.99)).tier == "client"


def test_win_arm64_full_tier_uses_gguf() -> None:
    plan = recommend(_hw(16.0, platform="Windows", arch="aarch64"))
    assert plan.tier == "full"
    assert plan.engine == "llamacpp"
    assert plan.format == "gguf"


def test_platform_and_machine_overrides_win_arm() -> None:
    # Hardware stub says Linux/x86_64, but explicit overrides force win-arm64.
    plan = recommend(_hw(6.0), platform_system="Windows", machine="arm64")
    assert plan.engine == "llamacpp"
    assert plan.format == "gguf"
    assert plan.tier == "lite"


def test_non_windows_arm_stays_litert_on_lite() -> None:
    # Linux ARM64 keeps litert on the lite tier (only Windows/ARM lacks wheels).
    plan = recommend(_hw(6.0, platform="Linux", arch="aarch64"))
    assert plan.engine == "litert"
    assert plan.format == "litertlm"
