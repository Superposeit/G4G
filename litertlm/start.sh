#!/bin/bash
# LiteRT-LM Bridge startup.
#
# Ensures a default on-device model is present, then serves the bridge. The
# model auto-downloads on first boot so a fresh deployment ships with a working
# model out of the box — no manual step. Override the source with LITERTLM_REPO
# / LITERTLM_FILENAME / LITERTLM_MODEL_PATH, and set HF_TOKEN for gated repos.
set -euo pipefail

MODEL_PATH="${LITERTLM_MODEL_PATH:-/models/gemma-4-E2B-it.litertlm}"
MODEL_DIR="$(dirname "$MODEL_PATH")"
MODEL_FILE="$(basename "$MODEL_PATH")"
REPO="${LITERTLM_REPO:-litert-community/gemma-4-E2B-it-litert-lm}"
# Sanity floor so a truncated/partial download is treated as missing (~100 MB).
MIN_BYTES="${LITERTLM_MIN_BYTES:-100000000}"

echo "============================================"
echo " LiteRT-LM Bridge startup"
echo "   model path : $MODEL_PATH"
echo "   repo       : $REPO"
echo "============================================"

# uv runs the bridge (PEP 723 inline deps); huggingface-hub does the download.
pip install --quiet --no-cache-dir uv huggingface-hub

mkdir -p "$MODEL_DIR"

model_ok() {
    [ -f "$MODEL_PATH" ] && [ "$(stat -c%s "$MODEL_PATH" 2>/dev/null || echo 0)" -ge "$MIN_BYTES" ]
}

if model_ok; then
    echo "==> Model already present ($(du -h "$MODEL_PATH" | cut -f1)); skipping download."
else
    echo "==> Auto-downloading default model (first boot; can take several minutes)..."
    for attempt in 1 2 3; do
        if python - "$REPO" "$MODEL_FILE" "$MODEL_DIR" <<'PYEOF'
import os
import sys

from huggingface_hub import hf_hub_download

repo, filename, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
path = hf_hub_download(
    repo_id=repo,
    filename=filename,
    local_dir=out_dir,
    token=os.environ.get("HF_TOKEN") or None,
)
print("downloaded ->", path)
PYEOF
        then
            echo "==> Download succeeded (attempt $attempt)."
            break
        fi
        echo "!! Download attempt $attempt failed."
        if [ "$attempt" -eq 3 ]; then
            echo "!! Model download failed after 3 attempts. Starting the bridge anyway."
            echo "!! Fixes: set HF_TOKEN (gated repos), check egress/disk, or override"
            echo "!!        LITERTLM_REPO / LITERTLM_FILENAME."
        else
            sleep 5
        fi
    done
fi

if model_ok; then
    echo "==> Model ready at $MODEL_PATH ($(du -h "$MODEL_PATH" | cut -f1))."
else
    echo "!! WARNING: no valid model at $MODEL_PATH — /health stays unhealthy until one is provided."
fi

echo "==> Starting bridge on ${LITERTLM_HOST:-0.0.0.0}:${LITERTLM_PORT:-8000} ..."
exec uv run bridge.py
