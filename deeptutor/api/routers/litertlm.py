"""
LiteRT-LM Model Management API Router

Provides endpoints for:
- Hardware detection and compatibility checking
- Model catalog (available models from Hugging Face)
- Downloaded models management
- Model download with progress tracking
- Model deletion and active model switching
"""

import asyncio
import json
import logging
import os
import platform
import re
import urllib.parse
import urllib.request
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from deeptutor.services.config.model_catalog import get_model_catalog_service

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Configuration ---

# Project root - resolve relative to this file
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_DEFAULT_MODELS_DIR = _PROJECT_ROOT / "data" / "models"

_env_model_path = os.environ.get("LITERTLM_MODEL_PATH", "")
if _env_model_path:
    _candidate = Path(_env_model_path)
    # If it points to a file, use parent dir
    if _candidate.suffix == ".litertlm":
        _candidate = _candidate.parent
    # Use env path only if it actually exists on this system
    _MODELS_DIR = _candidate if _candidate.exists() else _DEFAULT_MODELS_DIR
else:
    _MODELS_DIR = _DEFAULT_MODELS_DIR

HF_API_URL = "https://huggingface.co/api/models"
HF_ORG = "litert-community"

# --- Static model metadata (size/RAM estimates) ---
# HuggingFace API doesn't expose these, so we
# maintain a lookup for known models.
_KNOWN_MODEL_META: Dict[str, Dict[str, Any]] = {
    "gemma-4-E2B-it-litert-lm": {
        "size_gb": 1.4,
        "ram_gb": 3,
        "context_window": 8192,
        "min_ram_gb": 3,
        "tags_extra": ["mobile", "lightweight"],
        "description": "Gemma 4 E2B – 2.3B params, optimized for mobile devices",
    },
    "gemma-4-E4B-it-litert-lm": {
        "size_gb": 2.8,
        "ram_gb": 6,
        "context_window": 8192,
        "min_ram_gb": 6,
        "tags_extra": ["desktop", "balanced"],
        "description": "Gemma 4 E4B – 4.5B params, for laptops and desktops",
    },
    "Gemma3-1B-IT": {
        "size_gb": 0.6,
        "ram_gb": 2,
        "context_window": 8192,
        "min_ram_gb": 2,
        "tags_extra": ["mobile", "lightweight"],
        "description": "Gemma 3 1B IT – 1B params, ultra-lightweight",
    },
    "gemma-3-270m-it": {
        "size_gb": 0.2,
        "ram_gb": 1,
        "context_window": 8192,
        "min_ram_gb": 1,
        "tags_extra": ["tiny", "experimental"],
        "description": "Gemma 3 270M IT – 270M params, tiny model",
    },
    "Qwen2.5-1.5B-Instruct": {
        "size_gb": 0.9,
        "ram_gb": 2,
        "context_window": 4096,
        "min_ram_gb": 2,
        "tags_extra": ["lightweight"],
        "description": "Qwen 2.5 1.5B Instruct – versatile small model",
    },
    "Qwen2.5-0.5B-Instruct": {
        "size_gb": 0.3,
        "ram_gb": 1,
        "context_window": 4096,
        "min_ram_gb": 1,
        "tags_extra": ["tiny"],
        "description": "Qwen 2.5 0.5B Instruct – ultra-lightweight",
    },
    "Qwen3-0.6B": {
        "size_gb": 0.4,
        "ram_gb": 1,
        "context_window": 4096,
        "min_ram_gb": 1,
        "tags_extra": ["tiny"],
        "description": "Qwen 3 0.6B – small reasoning model",
    },
    "Qwen3-4B": {
        "size_gb": 2.5,
        "ram_gb": 5,
        "context_window": 8192,
        "min_ram_gb": 5,
        "tags_extra": ["desktop", "balanced"],
        "description": "Qwen 3 4B – strong desktop-class model",
    },
    "Qwen3-8B": {
        "size_gb": 5.0,
        "ram_gb": 10,
        "context_window": 8192,
        "min_ram_gb": 10,
        "tags_extra": ["large", "powerful"],
        "description": "Qwen 3 8B – large, high-quality model",
    },
    "Qwen3-14B": {
        "size_gb": 8.5,
        "ram_gb": 16,
        "context_window": 8192,
        "min_ram_gb": 16,
        "tags_extra": ["large", "powerful"],
        "description": "Qwen 3 14B – largest available, needs 16GB+ RAM",
    },
    "DeepSeek-R1-Distill-Qwen-1.5B": {
        "size_gb": 0.9,
        "ram_gb": 2,
        "context_window": 4096,
        "min_ram_gb": 2,
        "tags_extra": ["reasoning", "lightweight"],
        "description": "DeepSeek R1 Distill Qwen 1.5B – reasoning-focused",
    },
    "Phi-4-mini-instruct": {
        "size_gb": 2.3,
        "ram_gb": 5,
        "context_window": 4096,
        "min_ram_gb": 5,
        "tags_extra": ["desktop", "balanced"],
        "description": "Phi-4 Mini Instruct – Microsoft's compact model",
    },
    "SmolLM-135M-Instruct": {
        "size_gb": 0.1,
        "ram_gb": 0.5,
        "context_window": 2048,
        "min_ram_gb": 0.5,
        "tags_extra": ["tiny", "experimental"],
        "description": "SmolLM 135M – ultra-tiny chat model",
    },
    "SmolLM2-360M-Instruct": {
        "size_gb": 0.2,
        "ram_gb": 1,
        "context_window": 2048,
        "min_ram_gb": 1,
        "tags_extra": ["tiny"],
        "description": "SmolLM2 360M – small on-device chat model",
    },
    "TinyLlama-1.1B-Chat-v1.0": {
        "size_gb": 0.7,
        "ram_gb": 2,
        "context_window": 2048,
        "min_ram_gb": 2,
        "tags_extra": ["lightweight"],
        "description": "TinyLlama 1.1B Chat – compact Llama variant",
    },
    "FastVLM-0.5B": {
        "size_gb": 0.3,
        "ram_gb": 1,
        "context_window": 2048,
        "min_ram_gb": 1,
        "tags_extra": ["vision", "multimodal"],
        "description": "FastVLM 0.5B – lightweight vision-language model",
    },
    "functiongemma-270m-ft-mobile-actions": {
        "size_gb": 0.2,
        "ram_gb": 1,
        "context_window": 2048,
        "min_ram_gb": 1,
        "tags_extra": ["function-calling", "mobile"],
        "description": "FunctionGemma 270M – function calling for mobile",
    },
}

# Fallback defaults for unknown models
_DEFAULT_META = {
    "size_gb": 1.0,
    "ram_gb": 2,
    "context_window": 4096,
    "min_ram_gb": 2,
    "tags_extra": [],
    "description": "",
}

# --- Pydantic Models ---


class HardwareSpecs(BaseModel):
    cpu_model: str
    cpu_cores: int
    ram_total_gb: float
    ram_available_gb: float
    gpu_model: Optional[str] = None
    gpu_memory_gb: Optional[float] = None
    disk_total_gb: float
    disk_available_gb: float
    platform: str
    architecture: str


class ModelInfo(BaseModel):
    id: str
    name: str
    repo_id: str
    filename: str
    size_gb: float
    ram_gb: float
    context_window: int
    description: str
    min_cpu: str
    min_ram_gb: float
    tags: List[str]
    downloads: int = 0
    likes: int = 0


class DownloadedModelInfo(BaseModel):
    id: str
    name: str
    filename: str
    size_gb: float
    path: str
    download_date: str
    is_active: bool


class CompatibilityStatus(BaseModel):
    compatible: bool
    issues: List[str]
    warnings: List[str]


class ModelWithCompatibility(BaseModel):
    model: ModelInfo
    compatibility: CompatibilityStatus


class DownloadRequest(BaseModel):
    model_id: str


class DownloadResponse(BaseModel):
    task_id: str
    status: str
    message: str


class SetActiveModelRequest(BaseModel):
    model_id: str


class DeleteModelRequest(BaseModel):
    model_id: str


class DownloadProgress(BaseModel):
    task_id: str
    status: str
    progress: float
    downloaded_bytes: int
    total_bytes: int
    error: Optional[str] = None


class TokenRequest(BaseModel):
    token: str


# --- Hardware Detection ---


def _detect_cpu_model() -> str:
    """Detect CPU model name with multiple fallbacks."""
    # 1. platform.processor() — works on Windows/macOS
    cpu = platform.processor()
    if cpu and cpu.strip() and cpu.strip().lower() not in ("", "unknown"):
        return cpu.strip()

    # 2. /proc/cpuinfo — Linux (including Docker)
    try:
        cpuinfo = Path("/proc/cpuinfo").read_text()
        match = re.search(r"model name\s*:\s*(.+)", cpuinfo)
        if match:
            return match.group(1).strip()
    except (FileNotFoundError, PermissionError):
        pass

    # 3. lscpu fallback
    try:
        import subprocess
        result = subprocess.run(
            ["lscpu"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            match = re.search(r"Model name:\s*(.+)", result.stdout)
            if match:
                return match.group(1).strip()
    except Exception:
        pass

    return f"Unknown CPU ({platform.machine()})"


def get_hardware_specs() -> HardwareSpecs:
    """Detect system hardware specifications."""
    try:
        import psutil
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="psutil not installed. Install with: pip install psutil"
        )

    cpu_info = _detect_cpu_model()
    cpu_cores = psutil.cpu_count(logical=True) or 0

    ram = psutil.virtual_memory()
    ram_total_gb = round(ram.total / (1024**3), 2)
    ram_available_gb = round(ram.available / (1024**3), 2)

    gpu_model = None
    gpu_memory_gb = None

    # Try to detect GPU
    try:
        import torch

        if torch.cuda.is_available():
            gpu_model = torch.cuda.get_device_name(0)
            gpu_memory_gb = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            gpu_model = "Apple Metal (MPS)"
            gpu_memory_gb = None  # Metal doesn't expose memory easily
    except ImportError:
        pass

    # Use models directory for disk space — reflects actual storage available
    disk_path = _MODELS_DIR if _MODELS_DIR.exists() else _PROJECT_ROOT
    disk = psutil.disk_usage(str(disk_path))
    # Allow env override since Docker/WSL2 reports virtual disk, not host device
    disk_total_override = os.environ.get("DEVICE_DISK_TOTAL_GB", "")
    disk_total_gb = float(disk_total_override) if disk_total_override else round(disk.total / (1024**3), 2)
    disk_available_gb = round(disk.free / (1024**3), 2)

    return HardwareSpecs(
        cpu_model=cpu_info,
        cpu_cores=cpu_cores,
        ram_total_gb=ram_total_gb,
        ram_available_gb=ram_available_gb,
        gpu_model=gpu_model,
        gpu_memory_gb=gpu_memory_gb,
        disk_total_gb=disk_total_gb,
        disk_available_gb=disk_available_gb,
        platform=platform.system(),
        architecture=platform.machine(),
    )


def check_model_compatibility(hardware: HardwareSpecs, model: ModelInfo) -> CompatibilityStatus:
    """Check if hardware is compatible with a model."""
    issues = []
    warnings = []

    # Check RAM
    if hardware.ram_total_gb < model.min_ram_gb:
        issues.append(
            f"Insufficient RAM: {hardware.ram_total_gb}GB < {model.min_ram_gb}GB required"
        )
    elif hardware.ram_total_gb < model.min_ram_gb * 1.5:
        warnings.append(
            f"Low RAM: {hardware.ram_total_gb}GB (recommended: {model.min_ram_gb * 1.5}GB+)"
        )

    # Check disk space (need 50% buffer for download and extraction)
    required_disk = model.size_gb * 1.5
    if hardware.disk_available_gb < required_disk:
        issues.append(
            f"Insufficient disk space: {hardware.disk_available_gb}GB < {required_disk:.1f}GB required"
        )

    # Check CPU compatibility
    cpu_arch = hardware.architecture.lower()
    if "arm64" in cpu_arch or "aarch64" in cpu_arch:
        if "armv8" not in model.min_cpu.lower():
            issues.append(f"Incompatible CPU architecture: {hardware.architecture}")
    elif "x86_64" in cpu_arch or "amd64" in cpu_arch:
        if "x86_64" not in model.min_cpu.lower():
            issues.append(f"Incompatible CPU architecture: {hardware.architecture}")

    return CompatibilityStatus(
        compatible=len(issues) == 0,
        issues=issues,
        warnings=warnings,
    )


# --- HuggingFace Catalog Fetching ---

# Cache for fetched models (refreshed per-request is fine for settings page)
_catalog_cache: Optional[List[Dict[str, Any]]] = None
_catalog_cache_time: float = 0
_CACHE_TTL = 300  # 5 minutes


async def _fetch_hf_catalog(search: str = "") -> List[Dict[str, Any]]:
    """Fetch litert-lm models from HuggingFace API."""
    import time
    global _catalog_cache, _catalog_cache_time

    now = time.time()
    if _catalog_cache is not None and (now - _catalog_cache_time) < _CACHE_TTL and not search:
        return _catalog_cache

    params = {
        "author": HF_ORG,
        "sort": "downloads",
        "direction": "-1",
        "limit": "100",
    }
    if search:
        params["search"] = search

    try:
        query = urllib.parse.urlencode(params)
        url = f"{HF_API_URL}?{query}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        loop = asyncio.get_event_loop()
        resp_bytes = await loop.run_in_executor(
            None,
            partial(urllib.request.urlopen, req, timeout=15),
        )
        all_models = json.loads(resp_bytes.read())
    except Exception as e:
        logger.warning("Failed to fetch HuggingFace catalog: %s", e)
        return _catalog_cache or []

    # Filter to only litert-lm library models (text-generation)
    lm_models = [
        m for m in all_models
        if m.get("library_name") == "litert-lm"
    ]

    if not search:
        _catalog_cache = lm_models
        _catalog_cache_time = now

    return lm_models


def _hf_to_model_info(hf_model: Dict[str, Any]) -> ModelInfo:
    """Convert a HuggingFace API model dict to ModelInfo."""
    repo_id = hf_model["id"]  # e.g. "litert-community/gemma-4-E2B-it-litert-lm"
    model_name_slug = repo_id.split("/", 1)[-1]  # e.g. "gemma-4-E2B-it-litert-lm"

    meta = _KNOWN_MODEL_META.get(model_name_slug, _DEFAULT_META)

    # Derive human-readable name from slug
    display_name = model_name_slug.replace("-litert-lm", "").replace("-", " ").replace("_", " ")
    display_name = " ".join(w.capitalize() if not w[0].isdigit() else w for w in display_name.split())

    # Derive filename: slug + .litertlm
    # For repos like "gemma-4-E2B-it-litert-lm", filename = "gemma-4-E2B-it.litertlm"
    filename_base = model_name_slug.replace("-litert-lm", "").replace("-litert_lm", "")
    filename = f"{filename_base}.litertlm"

    hf_tags = hf_model.get("tags", [])
    combined_tags = meta.get("tags_extra", []) + [
        t for t in hf_tags
        if t in ("chat", "text-generation", "function-calling", "Conversational")
    ]

    description = meta.get("description") or f"{display_name} – LiteRT-LM optimized model"

    return ModelInfo(
        id=model_name_slug,
        name=display_name,
        repo_id=repo_id,
        filename=filename,
        size_gb=meta.get("size_gb", _DEFAULT_META["size_gb"]),
        ram_gb=meta.get("ram_gb", _DEFAULT_META["ram_gb"]),
        context_window=meta.get("context_window", _DEFAULT_META["context_window"]),
        description=description,
        min_cpu="ARMv8 or x86_64",
        min_ram_gb=meta.get("min_ram_gb", _DEFAULT_META["min_ram_gb"]),
        tags=combined_tags,
        downloads=hf_model.get("downloads", 0),
        likes=hf_model.get("likes", 0),
    )


# --- API Endpoints ---


@router.get("/hardware", response_model=HardwareSpecs)
async def get_hardware():
    """Get system hardware specifications."""
    return get_hardware_specs()


@router.get("/models/available", response_model=List[ModelWithCompatibility])
async def get_available_models(
    search: str = Query("", description="Search filter for model names"),
):
    """Get list of available LiteRT-LM models with compatibility info."""
    hardware = get_hardware_specs()
    hf_models = await _fetch_hf_catalog(search=search)

    result = []
    for hf_model in hf_models:
        model = _hf_to_model_info(hf_model)
        compatibility = check_model_compatibility(hardware, model)
        result.append(
            ModelWithCompatibility(
                model=model,
                compatibility=compatibility,
            )
        )

    return result


@router.get("/models/downloaded", response_model=List[DownloadedModelInfo])
async def get_downloaded_models():
    """Get list of downloaded LiteRT-LM models."""
    if not _MODELS_DIR.exists():
        return []

    # Determine which model is currently active
    active_env = os.environ.get("LITERTLM_MODEL_ID", "")
    active_model_path = os.environ.get("LITERTLM_MODEL_PATH", "")
    # If path points to a file, extract filename for matching
    active_path = Path(active_model_path) if active_model_path else None
    active_filename = active_path.name if active_path and active_path.suffix == ".litertlm" else ""

    result = []
    for model_file in _MODELS_DIR.glob("*.litertlm"):
        size_gb = round(model_file.stat().st_size / (1024**3), 2)
        download_date = datetime.fromtimestamp(model_file.stat().st_mtime).isoformat()

        # Derive model ID from filename: "gemma-4-E2B-it.litertlm" → "gemma-4-E2B-it"
        model_id = model_file.stem

        # Find display name from known metadata
        # Try matching against known slugs
        display_name = model_id
        for slug, meta in _KNOWN_MODEL_META.items():
            if slug.replace("-litert-lm", "") == model_id:
                display_name = meta.get("description", model_id).split("–")[0].strip()
                break
        else:
            display_name = model_id.replace("-", " ").replace("_", " ").title()

        # Check if this is the active model
        is_active = (
            model_file.name == active_filename
            or model_id == active_env
            or active_model_path == str(model_file)
        )

        result.append(
            DownloadedModelInfo(
                id=model_id,
                name=display_name,
                filename=model_file.name,
                size_gb=size_gb,
                path=str(model_file),
                download_date=download_date,
                is_active=is_active,
            )
        )

    return result


_DOWNLOAD_TASKS: Dict[str, Dict[str, Any]] = {}

def _download_thread(model_id: str, repo_id: str, target_filename: str, final_path: Path):
    try:
        import requests
        
        token = os.environ.get("HF_TOKEN")
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
            
        # Get download URL. Resolve redirect to get actual file URL
        api_url = f"https://huggingface.co/{repo_id}/resolve/main/{target_filename}"
        
        # Follow redirects to get LFS URL
        with requests.get(api_url, headers=headers, stream=True, allow_redirects=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            
            _DOWNLOAD_TASKS[model_id]["total_bytes"] = total_size
            _DOWNLOAD_TASKS[model_id]["status"] = "downloading"
            
            temp_path = final_path.with_suffix(".download")
            downloaded = 0
            
            with open(temp_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192 * 4):
                    if _DOWNLOAD_TASKS[model_id].get("cancel"):
                        break
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        _DOWNLOAD_TASKS[model_id]["downloaded_bytes"] = downloaded
                        if total_size > 0:
                            _DOWNLOAD_TASKS[model_id]["progress"] = downloaded / total_size
                            
            if _DOWNLOAD_TASKS[model_id].get("cancel"):
                temp_path.unlink(missing_ok=True)
                _DOWNLOAD_TASKS[model_id]["status"] = "cancelled"
            else:
                import shutil
                if final_path.exists():
                    final_path.unlink()
                shutil.move(temp_path, final_path)
                _DOWNLOAD_TASKS[model_id]["status"] = "completed"
                _DOWNLOAD_TASKS[model_id]["progress"] = 1.0
                
    except Exception as e:
        logger.error(f"Download error: {e}")
        _DOWNLOAD_TASKS[model_id]["status"] = "error"
        _DOWNLOAD_TASKS[model_id]["error"] = str(e)


@router.get("/models/download/progress", response_model=Dict[str, DownloadProgress])
async def get_download_progress():
    """Get active download tasks progress."""
    return _DOWNLOAD_TASKS


@router.delete("/models/download/{task_id}")
async def cancel_download(task_id: str):
    """Cancel an active download."""
    if task_id in _DOWNLOAD_TASKS:
        _DOWNLOAD_TASKS[task_id]["cancel"] = True
        return {"message": f"Cancelled task {task_id}"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/models/download", response_model=DownloadResponse)
async def download_model(request: DownloadRequest):
    """Download a LiteRT-LM model from Hugging Face."""
    model_id = request.model_id

    # Try to find model in catalog
    hf_models = await _fetch_hf_catalog()
    model_info = None
    for hf_model in hf_models:
        info = _hf_to_model_info(hf_model)
        if info.id == model_id:
            model_info = info
            break

    if not model_info:
        raise HTTPException(
            status_code=404,
            detail=f"Model {model_id} not found in catalog"
        )

    target_path = _MODELS_DIR / model_info.filename

    # Check if already downloaded
    if target_path.exists():
        return DownloadResponse(
            task_id=model_id,
            status="already_exists",
            message=f"Model {model_info.name} is already downloaded",
        )

    # Check disk space
    hardware = get_hardware_specs()
    required_disk = model_info.size_gb * 1.5
    if hardware.disk_available_gb < required_disk:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient disk space: {hardware.disk_available_gb}GB < {required_disk:.1f}GB required"
        )

    try:
        from huggingface_hub import HfApi
        import threading

        _MODELS_DIR.mkdir(parents=True, exist_ok=True)

        api = HfApi(token=os.environ.get("HF_TOKEN"))
        files = api.list_repo_files(model_info.repo_id)

        target_filename = None
        for ext in [".litertlm", ".tflite", ".task", ".bin"]:
            matches = [f for f in files if f.endswith(ext)]
            if matches:
                q8_matches = [f for f in matches if "q8" in f.lower()]
                target_filename = q8_matches[0] if q8_matches else matches[0]
                break

        if not target_filename:
            raise HTTPException(status_code=404, detail="No suitable .litertlm or .tflite file found in repo.")

        final_path = _MODELS_DIR / f"{model_id}.litertlm"
        
        _DOWNLOAD_TASKS[model_id] = {
            "task_id": model_id,
            "status": "pending",
            "progress": 0.0,
            "downloaded_bytes": 0,
            "total_bytes": 0,
            "cancel": False,
            "error": None
        }
        
        thread = threading.Thread(
            target=_download_thread,
            args=(model_id, model_info.repo_id, target_filename, final_path)
        )
        thread.start()

        return DownloadResponse(
            task_id=model_id,
            status="started",
            message=f"Model {model_info.name} download started",
        )
    except Exception as e:
        if model_id in _DOWNLOAD_TASKS:
            _DOWNLOAD_TASKS[model_id]["status"] = "error"
            _DOWNLOAD_TASKS[model_id]["error"] = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start download: {str(e)}"
        )


@router.delete("/models/{model_id}")
async def delete_model(model_id: str):
    """Delete a downloaded LiteRT-LM model."""
    if not _MODELS_DIR.exists():
        raise HTTPException(status_code=404, detail="Models directory not found")

    # Find the file
    target_path = _MODELS_DIR / f"{model_id}.litertlm"

    if not target_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Model {model_id} is not downloaded"
        )

    try:
        target_path.unlink()
        return {"message": f"Model {model_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete model: {str(e)}"
        )


@router.post("/models/active")
async def set_active_model(request: SetActiveModelRequest):
    """Set the active LiteRT-LM model."""
    model_id = request.model_id
    target_path = _MODELS_DIR / f"{model_id}.litertlm"

    if not target_path.exists():
        raise HTTPException(
            status_code=400,
            detail=f"Model {model_id} is not downloaded. Download it first."
        )

    # Update environment variable (note: this only affects the current process)
    os.environ["LITERTLM_MODEL_PATH"] = str(target_path)
    os.environ["LITERTLM_MODEL_ID"] = model_id

    # 1. Dynamically update the bridge
    bridge_port = os.environ.get("LITERTLM_PORT", "8000")
    try:
        # Docker internal name is 'litertlm', fallback to localhost
        bridge_host = "litertlm" if os.environ.get("DOCKER_ENV") else "localhost"
        requests.post(
            f"http://{bridge_host}:{bridge_port}/v1/models/active",
            json={"model_path": str(target_path), "model_id": model_id},
            timeout=5
        )
    except Exception as e:
        logger.warning(f"Could not dynamically notify bridge (it may need a restart): {e}")

    # 2. Update DeepTutor system catalog so the UI and .env reflect the change
    try:
        catalog_service = get_model_catalog_service()
        catalog = catalog_service.load()
        llm_profile = catalog_service.get_active_profile(catalog, "llm")
        llm_model = catalog_service.get_active_model(catalog, "llm")
        
        # Only overwrite if the user is currently using the litertlm bridge
        if llm_profile and llm_profile.get("binding") == "litertlm":
            if llm_model:
                llm_model["model"] = model_id
                llm_model["name"] = model_id
                catalog_service.apply(catalog)
    except Exception as e:
        logger.error(f"Failed to update model catalog: {e}")

    return {
        "message": f"Active model set to {model_id}",
        "model_path": str(target_path),
        "note": "Bridge updated successfully."
    }


@router.get("/models/token")
async def get_hf_token():
    """Get the current HF token from env (masked) or indicate if missing."""
    token = os.environ.get("HF_TOKEN", "")
    masked = f"{token[:4]}...{token[-4:]}" if len(token) > 8 else ("***" if token else "")
    return {"has_token": bool(token), "masked_token": masked}


@router.post("/models/token")
async def set_hf_token(request: TokenRequest):
    """Save HF token to .env and set it in environment."""
    token = request.token.strip()
    
    # Update current process
    os.environ["HF_TOKEN"] = token
    
    # Update .env file
    env_path = _PROJECT_ROOT / ".env"
    if env_path.exists():
        lines = env_path.read_text().splitlines()
        found = False
        for i, line in enumerate(lines):
            if line.startswith("HF_TOKEN="):
                lines[i] = f"HF_TOKEN={token}"
                found = True
                break
        if not found:
            lines.append(f"HF_TOKEN={token}")
        env_path.write_text("\n".join(lines) + "\n")
    
    return {"message": "Hugging Face token saved successfully"}
