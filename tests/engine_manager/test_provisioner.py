"""Tests for the engine-binary provisioner (download injected, no network)."""

from __future__ import annotations

import hashlib
import os

import pytest

from litertlm.engines import provisioner


def test_resolve_binary_path_shape(tmp_path) -> None:
    path = provisioner.resolve_binary("llamacpp", "win-x64", bin_root=str(tmp_path))
    assert path.endswith(os.path.join("llamacpp", "win-x64", "llama-server.exe"))


def test_resolve_binary_rejects_unknown_kind(tmp_path) -> None:
    with pytest.raises(ValueError, match="Unknown binary kind"):
        provisioner.resolve_binary("nope", "win-x64", bin_root=str(tmp_path))


def test_resolve_binary_rejects_unknown_platform(tmp_path) -> None:
    with pytest.raises(ValueError, match="Unsupported platform"):
        provisioner.resolve_binary("llamacpp", "solaris-sparc", bin_root=str(tmp_path))


def test_ensure_binary_noops_when_present(tmp_path) -> None:
    target = provisioner.resolve_binary("llamacpp", "win-x64", bin_root=str(tmp_path))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "wb") as fh:
        fh.write(b"already-here")

    calls: list[str] = []

    def downloader(url: str, dest: str) -> None:
        calls.append(url)

    result = provisioner.ensure_binary(
        "llamacpp", "win-x64", bin_root=str(tmp_path), downloader=downloader
    )

    assert result == target
    assert calls == []  # existing file → no download
    with open(target, "rb") as fh:
        assert fh.read() == b"already-here"


def test_ensure_binary_downloads_and_verifies(tmp_path) -> None:
    content = b"pretend-binary-bytes"
    checksum = hashlib.sha256(content).hexdigest()

    def downloader(url: str, dest: str) -> None:
        with open(dest, "wb") as fh:
            fh.write(content)

    result = provisioner.ensure_binary(
        "whisper",
        "linux-x64",
        bin_root=str(tmp_path),
        downloader=downloader,
        expected_sha256=checksum,
    )

    assert os.path.exists(result)
    with open(result, "rb") as fh:
        assert fh.read() == content


def test_ensure_binary_raises_on_checksum_mismatch(tmp_path) -> None:
    def downloader(url: str, dest: str) -> None:
        with open(dest, "wb") as fh:
            fh.write(b"tampered")

    with pytest.raises(ValueError, match="Checksum mismatch"):
        provisioner.ensure_binary(
            "llamacpp",
            "linux-arm64",
            bin_root=str(tmp_path),
            downloader=downloader,
            expected_sha256="deadbeef" * 8,
        )

    # The untrusted artifact must be removed so a retry re-downloads cleanly.
    target = provisioner.resolve_binary("llamacpp", "linux-arm64", bin_root=str(tmp_path))
    assert not os.path.exists(target)


def test_ensure_binary_requires_downloader_when_missing(tmp_path) -> None:
    with pytest.raises(RuntimeError, match="no downloader"):
        provisioner.ensure_binary("llamacpp", "win-arm64", bin_root=str(tmp_path))
