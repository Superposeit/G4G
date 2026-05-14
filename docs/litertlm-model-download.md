# LiteRT-LM Model Download Guide

**Project:** DeepTutor (G4G Hackathon)
**Model:** Gemma 4 E2B (2.3B parameters)
**Format:** .litertlm (LiteRT-LM format)
**Size:** ~1.2 GB

---

## Overview

This guide covers downloading the Gemma 4 E2B model in LiteRT-LM format for use with the
LiteRT-LM Bridge.

**Note:** When using Docker Compose, the model is downloaded automatically on first startup.
See the [Docker workflow](#docker-workflow) section below.

---

## Quick Start

### 1. In-App UI Download (New & Recommended)

You can now browse, download, and manage models directly from the web interface:

1. Open the **Settings** page in the DeepTutor app.
2. Navigate to the **LiteRT-LM** tab.
3. Browse the **Catalog** of available models.
4. Click **Download** on any compatible model.
5. Track the download progress and cancel if needed in the **Downloaded Models** section.

### 2. Docker Compose (Auto-download)

The model is downloaded automatically when you start the services:

```bash
# Start all services (model downloads on first startup)
docker compose up -d

# View logs to see download progress
docker compose logs -f litertlm

# The model is persisted in a Docker volume
docker volume ls | grep litertlm
```

### Using the Download Script

If you prefer to download the model manually:

```bash
# Download default model (gemma-4-E2B-it)
python scripts/download_litertlm_model.py

# Download a specific repo/file
python scripts/download_litertlm_model.py \
    --repo litert-community/gemma-4-E2B-it-litert-lm \
    --filename gemma-4-E2B-it.litertlm

# Override output directory
python scripts/download_litertlm_model.py --output-dir /mnt/models
```

---

## How the path is resolved (priority order)

| Priority | Source | Value |
|----------|--------|-------|
| 1 | `LITERTLM_MODEL_PATH` env var | Absolute path set by you / CI / docker-compose |
| 2 | Script default | `<project-root>/data/models/gemma-4-E2B-it.litertlm` |

`bridge.py` uses the same priority. `docker-compose.yml` mounts
`${LITERTLM_MODEL_PATH}` (host path) as `/model.litertlm` inside the container
and injects `LITERTLM_MODEL_PATH=/model.litertlm`.

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LITERTLM_MODEL_PATH` | `data/models/gemma-4-E2B-it.litertlm` | Absolute path to the `.litertlm` file used by `bridge.py` and `docker-compose.yml` |
| `LITERTLM_REPO` | `litert-community/gemma-4-E2B-it-litert-lm` | HuggingFace repo id |
| `LITERTLM_FILENAME` | `gemma-4-E2B-it.litertlm` | Filename inside the repo |
| `LITERTLM_OUTPUT_DIR` | `<project-root>/data/models` | Directory where the file is saved |
| `HF_TOKEN` | _(empty)_ | HuggingFace token — only needed for gated models |
| `LITERTLM_HOST` | `0.0.0.0` | Host to bind the bridge server to |
| `LITERTLM_PORT` | `8000` | Port to bind the bridge server to |
| `LITERTLM_MODEL_ID` | `gemma-4-E2B-it` | Model ID to report in API responses |
| `LITERTLM_LOG_LEVEL` | `INFO` | Logging level for the bridge (DEBUG, INFO, WARNING, ERROR) |

Set any of these in `.env` before running the script, or pass them as CLI flags.

---

## CLI flags

```
python scripts/download_litertlm_model.py [options]

  --repo        HF repo id      (overrides LITERTLM_REPO)
  --filename    Model filename  (overrides LITERTLM_FILENAME)
  --output-dir  Output dir      (overrides LITERTLM_OUTPUT_DIR)
  --hf-token    HF token        (overrides HF_TOKEN)
```

### Examples

```bash
# Default model, default output dir
python scripts/download_litertlm_model.py

# Different model
python scripts/download_litertlm_model.py \
    --repo litert-community/gemma-4-1B-it-litert-lm \
    --filename gemma-4-1B-it.litertlm

# Store on a fast SSD instead of the project tree
python scripts/download_litertlm_model.py --output-dir D:/models

# Gated model with HF token
HF_TOKEN=hf_xxx python scripts/download_litertlm_model.py
```

---

## What the script does

1. Auto-installs `huggingface_hub` if missing (uses `pip` quietly).
2. Creates `LITERTLM_OUTPUT_DIR` if it does not exist.
3. Calls `hf_hub_download` — resumes interrupted downloads, skips if already cached.
4. Prints the resolved absolute path.
5. Patches `LITERTLM_MODEL_PATH` in `.env` (in-place, non-destructive).

---

## Docker workflow

The Docker Compose setup handles model download automatically:

```bash
# 1. Start all services (model downloads on first startup)
docker compose up -d

# 2. Watch the logs to see download progress
docker compose logs -f litertlm

# 3. Once healthy, the bridge is ready
curl http://localhost:8000/health
```

The model is persisted in a Docker volume named `litertlm-models` and will be reused
across container restarts. No rebuild required when the model file changes.

### Manual Model Download for Docker

If you want to download the model separately and use it with Docker:

```bash
# 1. Download the model
python scripts/download_litertlm_model.py --output-dir ./data/models

# 2. Update .env with the path
echo "LITERTLM_MODEL_PATH=$(pwd)/data/models/gemma-4-E2B-it.litertlm" >> .env

# 3. Start services
docker compose up -d
```

Note: The default Docker setup uses a volume for better portability. Using a host
path requires additional volume configuration in docker-compose.yml.

---

## CI / unattended environments

Export the variable before running compose:

```bash
export LITERTLM_MODEL_PATH=/shared/models/gemma-4-E2B-it.litertlm
python scripts/download_litertlm_model.py \
    --output-dir "$(dirname $LITERTLM_MODEL_PATH)"
docker compose --profile litertlm up -d
```

Or pre-download in a CI step and cache `data/models/` between runs.

---

## Supported models

Any `.litertlm` file published to HuggingFace Hub works. Known repos:

| Model | Repo | File |
|-------|------|------|
| Gemma-4 E2B (default) | `litert-community/gemma-4-E2B-it-litert-lm` | `gemma-4-E2B-it.litertlm` |

Add more rows here as the LiteRT-community publishes new weights.
