"""Engine-binary provisioning.

Resolves and (when needed) downloads the platform-specific ``llama-server`` and
``whisper`` binaries from PINNED, CHECKSUMMED releases. The actual download is
injected so tests exercise the verify/no-op logic without touching the network,
and no real binary is ever fetched here.

Supported platform keys: ``win-x64``, ``win-arm64``, ``linux-x64``,
``linux-arm64``.
"""

from __future__ import annotations

import hashlib
import os
import platform
from typing import Callable, Dict, Optional

# Repo root: litertlm/engines/provisioner.py -> project root.
_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
_DEFAULT_BIN_ROOT = os.path.join(_PROJECT_ROOT, "data", "bin")

_SUPPORTED_PLATFORMS = frozenset(
    {"win-x64", "win-arm64", "linux-x64", "linux-arm64"}
)

# Pinned releases per (kind, platform_key). Checksums are placeholders until the
# real release artifacts are pinned — see the TODO markers below.
# TODO: pin real checksum before release
_PINNED: Dict[str, Dict[str, dict]] = {
    "llamacpp": {
        "win-x64": {
            "version": "b4585",
            "url": "https://github.com/ggml-org/llama.cpp/releases/download/b4585/llama-b4585-bin-win-avx2-x64.zip",
            "binary": "llama-server.exe",
            "sha256": "0" * 64,  # TODO: pin real checksum before release
        },
        "win-arm64": {
            "version": "b4585",
            "url": "https://github.com/ggml-org/llama.cpp/releases/download/b4585/llama-b4585-bin-win-arm64.zip",
            "binary": "llama-server.exe",
            "sha256": "0" * 64,  # TODO: pin real checksum before release
        },
        "linux-x64": {
            "version": "b4585",
            "url": "https://github.com/ggml-org/llama.cpp/releases/download/b4585/llama-b4585-bin-ubuntu-x64.zip",
            "binary": "llama-server",
            "sha256": "0" * 64,  # TODO: pin real checksum before release
        },
        "linux-arm64": {
            "version": "b4585",
            "url": "https://github.com/ggml-org/llama.cpp/releases/download/b4585/llama-b4585-bin-ubuntu-arm64.zip",
            "binary": "llama-server",
            "sha256": "0" * 64,  # TODO: pin real checksum before release
        },
    },
    "whisper": {
        "win-x64": {
            "version": "1.7.4",
            "url": "https://github.com/ggml-org/whisper.cpp/releases/download/v1.7.4/whisper-bin-x64.zip",
            "binary": "whisper-server.exe",
            "sha256": "0" * 64,  # TODO: pin real checksum before release
        },
        "win-arm64": {
            "version": "1.7.4",
            "url": "https://github.com/ggml-org/whisper.cpp/releases/download/v1.7.4/whisper-bin-arm64.zip",
            "binary": "whisper-server.exe",
            "sha256": "0" * 64,  # TODO: pin real checksum before release
        },
        "linux-x64": {
            "version": "1.7.4",
            "url": "https://github.com/ggml-org/whisper.cpp/releases/download/v1.7.4/whisper-bin-ubuntu-x64.zip",
            "binary": "whisper-server",
            "sha256": "0" * 64,  # TODO: pin real checksum before release
        },
        "linux-arm64": {
            "version": "1.7.4",
            "url": "https://github.com/ggml-org/whisper.cpp/releases/download/v1.7.4/whisper-bin-ubuntu-arm64.zip",
            "binary": "whisper-server",
            "sha256": "0" * 64,  # TODO: pin real checksum before release
        },
    },
}


def current_platform_key() -> str:
    """Return the platform key for the host, e.g. ``"win-x64"``.

    Raises:
        RuntimeError: if the host OS/arch is not among the supported keys.
    """
    system = platform.system().lower()
    machine = platform.machine().lower()
    os_part = "win" if system.startswith("win") else "linux" if system == "linux" else system
    if machine in ("arm64", "aarch64"):
        arch_part = "arm64"
    elif machine in ("x86_64", "amd64", "x64"):
        arch_part = "x64"
    else:
        arch_part = machine
    key = f"{os_part}-{arch_part}"
    if key not in _SUPPORTED_PLATFORMS:
        raise RuntimeError(f"Unsupported platform: {system}/{machine} -> {key}")
    return key


def _pinned_entry(kind: str, platform_key: str) -> dict:
    """Look up the pinned release entry, validating ``kind``/``platform_key``."""
    if kind not in _PINNED:
        raise ValueError(f"Unknown binary kind: {kind!r} (expected one of {sorted(_PINNED)})")
    by_platform = _PINNED[kind]
    if platform_key not in by_platform:
        raise ValueError(
            f"Unsupported platform {platform_key!r} for {kind!r} "
            f"(expected one of {sorted(by_platform)})"
        )
    return by_platform[platform_key]


def resolve_binary(kind: str, platform_key: str, *, bin_root: Optional[str] = None) -> str:
    """Return the local path where the ``kind`` binary lives for ``platform_key``.

    This is pure path computation — it does not check for existence.

    Args:
        kind: ``"llamacpp"`` or ``"whisper"``.
        platform_key: One of the supported platform keys.
        bin_root: Override for the binaries root directory.
    """
    entry = _pinned_entry(kind, platform_key)
    root = bin_root or _DEFAULT_BIN_ROOT
    return os.path.join(root, kind, platform_key, entry["binary"])


def _sha256(path: str) -> str:
    """Compute the hex SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def ensure_binary(
    kind: str,
    platform_key: str,
    *,
    bin_root: Optional[str] = None,
    downloader: Optional[Callable[[str, str], None]] = None,
    expected_sha256: Optional[str] = None,
    verify: bool = True,
) -> str:
    """Ensure the ``kind`` binary exists locally, downloading + verifying if not.

    No-ops when the target file is already present. Otherwise the injected
    ``downloader(url, dest_path)`` fetches it, the SHA-256 is verified against the
    pinned (or overridden) checksum, and a mismatch raises.

    Args:
        kind: ``"llamacpp"`` or ``"whisper"``.
        platform_key: One of the supported platform keys.
        bin_root: Override for the binaries root directory.
        downloader: Callable writing the release to the given destination path.
            Required when a download is needed; injected in tests.
        expected_sha256: Overrides the pinned checksum (used to drive tests while
            real checksums remain placeholders).
        verify: When ``True``, verify the SHA-256 after download.

    Returns:
        The local path to the binary.

    Raises:
        ValueError: on checksum mismatch or unknown kind/platform.
        RuntimeError: if a download is required but no ``downloader`` was given.
    """
    entry = _pinned_entry(kind, platform_key)
    target = resolve_binary(kind, platform_key, bin_root=bin_root)

    if os.path.exists(target):
        return target

    if downloader is None:
        raise RuntimeError(
            f"{kind} binary missing at {target} and no downloader was provided"
        )

    os.makedirs(os.path.dirname(target), exist_ok=True)
    downloader(entry["url"], target)

    if verify:
        want = expected_sha256 if expected_sha256 is not None else entry["sha256"]
        got = _sha256(target)
        if got != want:
            # Remove the untrusted artifact so a retry re-downloads cleanly.
            try:
                os.remove(target)
            except OSError:
                pass
            raise ValueError(
                f"Checksum mismatch for {kind}/{platform_key}: expected {want}, got {got}"
            )

    return target
