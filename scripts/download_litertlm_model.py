#!/usr/bin/env python3
"""
download_litertlm_model.py
──────────────────────────
Downloads a LiteRT-LM model from Hugging Face Hub into a known project-local
path and prints the resolved path for use in LITERTLM_MODEL_PATH.

Usage
─────
  # Download default model (gemma-4-E2B-it)
  python scripts/download_litertlm_model.py

  # Download a specific repo/file
  python scripts/download_litertlm_model.py \
      --repo litert-community/gemma-4-E2B-it-litert-lm \
      --filename gemma-4-E2B-it.litertlm

  # Override output directory
  python scripts/download_litertlm_model.py --output-dir /mnt/models

Environment variables (all optional — CLI flags take precedence)
────────────────────────────────────────────────────────────────
  LITERTLM_REPO        HF repo id   (default: litert-community/gemma-4-E2B-it-litert-lm)
  LITERTLM_FILENAME    Model file   (default: gemma-4-E2B-it.litertlm)
  LITERTLM_OUTPUT_DIR  Output dir   (default: <project-root>/data/models)
  HF_TOKEN             HF access token for gated repos (optional)

After a successful download the script prints:
  LITERTLM_MODEL_PATH=<absolute path to .litertlm file>

Paste that line into your .env or export it before running docker compose.
"""

import argparse
import os
import sys
from pathlib import Path

# ── project root = two levels up from this script ────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_REPO     = "litert-community/gemma-4-E2B-it-litert-lm"
DEFAULT_FILENAME = "gemma-4-E2B-it.litertlm"
DEFAULT_OUT_DIR  = PROJECT_ROOT / "data" / "models"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Download a LiteRT-LM model from Hugging Face Hub.")
    p.add_argument("--repo",       default=None, help="HF repo id  (env: LITERTLM_REPO)")
    p.add_argument("--filename",   default=None, help="Model file  (env: LITERTLM_FILENAME)")
    p.add_argument("--output-dir", default=None, help="Output dir  (env: LITERTLM_OUTPUT_DIR)")
    p.add_argument("--hf-token",   default=None, help="HF token for gated repos (env: HF_TOKEN)")
    return p.parse_args()


def resolve(cli_val: str | None, env_key: str, default: str) -> str:
    return cli_val or os.environ.get(env_key) or default


def ensure_huggingface_hub() -> None:
    try:
        import huggingface_hub  # noqa: F401
    except ImportError:
        print("[download_litertlm] huggingface_hub not found — installing …")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub", "-q"])


def download_model(repo: str, filename: str, output_dir: Path, token: str | None) -> Path:
    from huggingface_hub import hf_hub_download

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[download_litertlm] repo     : {repo}")
    print(f"[download_litertlm] filename : {filename}")
    print(f"[download_litertlm] dest dir : {output_dir}")
    print("[download_litertlm] downloading … (this may take a while for large models)")

    local_path = hf_hub_download(
        repo_id=repo,
        filename=filename,
        local_dir=str(output_dir),
        token=token,
    )
    return Path(local_path).resolve()


def patch_env_file(model_path: Path) -> None:
    """If .env exists in project root, update / add LITERTLM_MODEL_PATH in-place."""
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        return

    lines = env_file.read_text(encoding="utf-8").splitlines(keepends=True)
    new_line = f"LITERTLM_MODEL_PATH={model_path}\n"
    found = False
    for i, line in enumerate(lines):
        if line.startswith("LITERTLM_MODEL_PATH="):
            lines[i] = new_line
            found = True
            break
    if not found:
        lines.append("\n" + new_line)

    env_file.write_text("".join(lines), encoding="utf-8")
    print(f"[download_litertlm] .env updated → LITERTLM_MODEL_PATH={model_path}")


def main() -> None:
    args = parse_args()

    repo       = resolve(args.repo,       "LITERTLM_REPO",       DEFAULT_REPO)
    filename   = resolve(args.filename,   "LITERTLM_FILENAME",   DEFAULT_FILENAME)
    output_dir = Path(resolve(args.output_dir, "LITERTLM_OUTPUT_DIR", str(DEFAULT_OUT_DIR)))
    token      = args.hf_token or os.environ.get("HF_TOKEN")

    ensure_huggingface_hub()

    model_path = download_model(repo, filename, output_dir, token)

    print(f"\n[download_litertlm] ✓ model ready at:\n  {model_path}")
    print(f"\nAdd to your .env:\n  LITERTLM_MODEL_PATH={model_path}")

    patch_env_file(model_path)


if __name__ == "__main__":
    main()
