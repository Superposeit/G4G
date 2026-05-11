#!/bin/bash
set -e

echo "============================================"
echo "LiteRT-LM Bridge Startup"
echo "============================================"

# Install dependencies
echo "Installing dependencies..."
pip install uv huggingface-hub -q

# Download model if not present
if [ ! -f /models/gemma-4-E2B-it.litertlm ]; then
    echo "Downloading Gemma 4 E2B model (this may take a while)..."
    python -c "from huggingface_hub import hf_hub_download; import os; os.makedirs('/models', exist_ok=True); hf_hub_download(repo_id='litert-community/gemma-4-E2B-it-litert-lm', filename='gemma-4-E2B-it.litertlm', local_dir='/models', repo_type='model')"
    echo "Model download complete!"
else
    echo "Model already exists, skipping download."
fi

# Start the bridge
echo "Starting LiteRT-LM Bridge..."
uv run bridge.py
