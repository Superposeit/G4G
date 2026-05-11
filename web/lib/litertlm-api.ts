// API client functions for LiteRT-LM model management

import { apiFetch, apiUrl } from "./api";

// ============================================
// Types
// ============================================

export interface HardwareSpecs {
  cpu_model: string;
  cpu_cores: number;
  ram_total_gb: number;
  ram_available_gb: number;
  gpu_model?: string;
  gpu_memory_gb?: number;
  disk_total_gb: number;
  disk_available_gb: number;
  platform: string;
  architecture: string;
}

export interface ModelInfo {
  id: string;
  name: string;
  repo_id: string;
  filename: string;
  size_gb: number;
  ram_gb: number;
  context_window: number;
  description: string;
  min_cpu: string;
  min_ram_gb: number;
  tags: string[];
}

export interface CompatibilityStatus {
  compatible: boolean;
  issues: string[];
  warnings: string[];
}

export interface ModelWithCompatibility {
  model: ModelInfo;
  compatibility: CompatibilityStatus;
}

export interface DownloadedModelInfo {
  id: string;
  name: string;
  filename: string;
  size_gb: number;
  path: string;
  download_date: string;
  is_active: boolean;
}

export interface DownloadRequest {
  model_id: string;
}

export interface DownloadResponse {
  task_id: string;
  status: string;
  message: string;
}

export interface SetActiveModelRequest {
  model_id: string;
}

// ============================================
// API Functions
// ============================================

/**
 * Get system hardware specifications
 */
export async function getHardwareSpecs(): Promise<HardwareSpecs> {
  const response = await apiFetch(apiUrl("/api/v1/litertlm/hardware"));
  if (!response.ok) {
    throw new Error(`Failed to get hardware specs: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Get list of available LiteRT-LM models with compatibility info
 */
export async function getAvailableModels(): Promise<ModelWithCompatibility[]> {
  const response = await apiFetch(apiUrl("/api/v1/litertlm/models/available"));
  if (!response.ok) {
    throw new Error(`Failed to get available models: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Get list of downloaded LiteRT-LM models
 */
export async function getDownloadedModels(): Promise<DownloadedModelInfo[]> {
  const response = await apiFetch(apiUrl("/api/v1/litertlm/models/downloaded"));
  if (!response.ok) {
    throw new Error(`Failed to get downloaded models: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Download a LiteRT-LM model from Hugging Face
 */
export async function downloadModel(
  modelId: string
): Promise<DownloadResponse> {
  const response = await apiFetch(apiUrl("/api/v1/litertlm/models/download"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model_id: modelId }),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `Failed to download model: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Delete a downloaded LiteRT-LM model
 */
export async function deleteModel(modelId: string): Promise<{ message: string }> {
  const response = await apiFetch(apiUrl(`/api/v1/litertlm/models/${modelId}`), {
    method: "DELETE",
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `Failed to delete model: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Set the active LiteRT-LM model
 */
export async function setActiveModel(
  modelId: string
): Promise<{ message: string; model_path: string; note: string }> {
  const response = await apiFetch(apiUrl("/api/v1/litertlm/models/active"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model_id: modelId }),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `Failed to set active model: ${response.statusText}`);
  }
  return response.json();
}
