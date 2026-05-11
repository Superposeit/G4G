"""
LiteRT-LM Model Management API Router

Provides endpoints for:
- Hardware detection and compatibility checking
- Model catalog (available models from Hugging Face)
- Downloaded models management
- Model download with progress tracking
- Model deletion and active model switching
"""

import os
import platform
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

# ============================================
# Configuration
# ============================================

# Project root - resolve relative to this file
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_MODELS_DIR = _PROJECT_ROOT / "data" / "models"

# ============================================
# Model Catalog
# ============================================

LITERTLM_MODELS: Dict[str, Dict[str, Any]] = {
    "gemma-4-E2B-it": {
        "id": "gemma-4-E2B-it",
        "name": "Gemma 4 E2B",
        "repo_id": "litert-community/gemma-4-E2B-it-litert-lm",
        "filename": "gemma-4-E2B-it.litertlm",
        "size_gb": 1.4,
        "ram_gb": 3,
        "context_window": 8192,
        "description": "Gemma 4 E2B - 2.3B parameters, optimized for mobile devices",
        "min_cpu": "ARMv8 or x86_64",
        "min_ram_gb": 3,
        "tags": ["mobile", "lightweight"],
    },
    "gemma-4-E4B-it": {
        "id": "gemma-4-E4B-it",
        "name": "Gemma 4 E4B",
        "repo_id": "litert-community/gemma-4-E4B-it-litert-lm",
        "filename": "gemma-4-E4B-it.litertlm",
        "size_gb": 2.8,
        "ram_gb": 6,
        "context_window": 8192,
        "description": "Gemma 4 E4B - 4.5B parameters, for laptops and desktops",
        "min_cpu": "ARMv8 or x86_64",
        "min_ram_gb": 6,
        "tags": ["desktop", "balanced"],
    },
}

# ============================================
# Pydantic Models
# ============================================


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


# ============================================
# Hardware Detection
# ============================================


def get_hardware_specs() -> HardwareSpecs:
    """Detect system hardware specifications."""
    try:
        import psutil
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="psutil not installed. Install with: pip install psutil"
        )

    cpu_info = platform.processor() or "Unknown CPU"
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

    disk = psutil.disk_usage(str(_PROJECT_ROOT))
    disk_total_gb = round(disk.total / (1024**3), 2)
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


# ============================================
# API Endpoints
# ============================================


@router.get("/hardware", response_model=HardwareSpecs)
async def get_hardware():
    """Get system hardware specifications."""
    return get_hardware_specs()


@router.get("/models/available", response_model=List[ModelWithCompatibility])
async def get_available_models():
    """Get list of available LiteRT-LM models with compatibility info."""
    hardware = get_hardware_specs()

    result = []
    for model_id, model_data in LITERTLM_MODELS.items():
        model = ModelInfo(**model_data)
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

    # Get active model path from environment
    active_model_path = os.environ.get("LITERTLM_MODEL_PATH", "")
    active_filename = Path(active_model_path).name if active_model_path else ""

    result = []
    for model_file in _MODELS_DIR.glob("*.litertlm"):
        # Find matching model in catalog
        model_info = None
        for catalog_model in LITERTLM_MODELS.values():
            if catalog_model["filename"] == model_file.name:
                model_info = catalog_model
                break

        if not model_info:
            continue

        size_gb = round(model_file.stat().st_size / (1024**3), 2)
        download_date = datetime.fromtimestamp(model_file.stat().st_mtime).isoformat()

        result.append(
            DownloadedModelInfo(
                id=model_info["id"],
                name=model_info["name"],
                filename=model_file.name,
                size_gb=size_gb,
                path=str(model_file),
                download_date=download_date,
                is_active=model_file.name == active_filename,
            )
        )

    return result


@router.post("/models/download", response_model=DownloadResponse)
async def download_model(request: DownloadRequest):
    """Download a LiteRT-LM model from Hugging Face."""
    model_id = request.model_id

    if model_id not in LITERTLM_MODELS:
        raise HTTPException(
            status_code=404,
            detail=f"Model {model_id} not found in catalog"
        )

    model = LITERTLM_MODELS[model_id]
    target_path = _MODELS_DIR / model["filename"]

    # Check if already downloaded
    if target_path.exists():
        return DownloadResponse(
            task_id=model_id,
            status="already_exists",
            message=f"Model {model['name']} is already downloaded",
        )

    # Check disk space
    hardware = get_hardware_specs()
    required_disk = model["size_gb"] * 1.5
    if hardware.disk_available_gb < required_disk:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient disk space: {hardware.disk_available_gb}GB < {required_disk:.1f}GB required"
        )

    try:
        from huggingface_hub import hf_hub_download

        _MODELS_DIR.mkdir(parents=True, exist_ok=True)

        hf_hub_download(
            repo_id=model["repo_id"],
            filename=model["filename"],
            local_dir=str(_MODELS_DIR),
        )

        return DownloadResponse(
            task_id=model_id,
            status="completed",
            message=f"Model {model['name']} downloaded successfully",
        )
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="huggingface_hub not installed. Install with: pip install huggingface_hub"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download model: {str(e)}"
        )


@router.delete("/models/{model_id}")
async def delete_model(model_id: str):
    """Delete a downloaded LiteRT-LM model."""
    if model_id not in LITERTLM_MODELS:
        raise HTTPException(
            status_code=404,
            detail=f"Model {model_id} not found in catalog"
        )

    model = LITERTLM_MODELS[model_id]
    target_path = _MODELS_DIR / model["filename"]

    if not target_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Model {model['name']} is not downloaded"
        )

    try:
        target_path.unlink()
        return {"message": f"Model {model['name']} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete model: {str(e)}"
        )


@router.post("/models/active")
async def set_active_model(request: SetActiveModelRequest):
    """Set the active LiteRT-LM model."""
    model_id = request.model_id

    if model_id not in LITERTLM_MODELS:
        raise HTTPException(
            status_code=404,
            detail=f"Model {model_id} not found in catalog"
        )

    model = LITERTLM_MODELS[model_id]
    target_path = _MODELS_DIR / model["filename"]

    if not target_path.exists():
        raise HTTPException(
            status_code=400,
            detail=f"Model {model['name']} is not downloaded. Download it first."
        )

    # Update environment variable (note: this only affects the current process)
    os.environ["LITERTLM_MODEL_PATH"] = str(target_path)

    return {
        "message": f"Active model set to {model['name']}",
        "model_path": str(target_path),
        "note": "Restart the LiteRT-LM bridge service for changes to take effect"
    }
