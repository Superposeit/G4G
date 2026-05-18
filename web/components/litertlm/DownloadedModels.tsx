"use client";

import { useEffect, useState } from "react";
import {
  Trash2,
  CheckCircle2,
  Loader2,
  AlertTriangle,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import {
  getDownloadedModels,
  deleteModel,
  setActiveModel,
  getDownloadProgress,
  cancelDownload,
  type DownloadedModelInfo,
  type DownloadProgress,
} from "@/lib/litertlm-api";

export default function DownloadedModels() {
  const { t } = useTranslation();
  const [downloadedModels, setDownloadedModels] = useState<DownloadedModelInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);
  const [activating, setActivating] = useState<string | null>(null);
  const [toast, setToast] = useState<{ message: string; type: "error" | "success" } | null>(null);
  const [activeDownloads, setActiveDownloads] = useState<Record<string, DownloadProgress>>({});

  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(null), 5000);
    return () => clearTimeout(timer);
  }, [toast]);

  const fetchModels = async () => {
    try {
      const data = await getDownloadedModels();
      setDownloadedModels(data);
      setLoading(false);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load downloaded models");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModels();
  }, []);

  useEffect(() => {
    let lastCompletedCount = 0;
    const interval = setInterval(async () => {
      try {
        const progress = await getDownloadProgress();
        setActiveDownloads(progress);
        
        const completedCount = Object.values(progress).filter(p => p.status === "completed").length;
        if (completedCount > lastCompletedCount) {
          lastCompletedCount = completedCount;
          fetchModels();
        }
      } catch (e) {
        console.error("Polling progress error:", e);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleDelete = async (modelId: string) => {
    if (!confirm("Are you sure you want to delete this model?")) {
      return;
    }

    setDeleting(modelId);
    try {
      await deleteModel(modelId);
      // Refresh downloaded models
      const data = await getDownloadedModels();
      setDownloadedModels(data);
      setToast({ message: "Model deleted successfully", type: "success" });
    } catch (e) {
      console.error("Failed to delete model:", e);
      setToast({
        message: e instanceof Error ? e.message : "Failed to delete model",
        type: "error",
      });
    } finally {
      setDeleting(null);
    }
  };

  const handleSetActive = async (modelId: string) => {
    setActivating(modelId);
    try {
      const result = await setActiveModel(modelId);
      setToast({ message: `${result.message}\n\n${result.note}`, type: "success" });
      // Refresh downloaded models to update active status
      const data = await getDownloadedModels();
      setDownloadedModels(data);
    } catch (e) {
      console.error("Failed to set active model:", e);
      setToast({
        message: e instanceof Error ? e.message : "Failed to set active model",
        type: "error",
      });
    } finally {
      setActivating(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-6 w-6 animate-spin text-[var(--muted-foreground)]" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-red-200 bg-red-50 p-6 dark:border-red-900/30 dark:bg-red-900/10">
        <div className="flex items-start gap-3">
          <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-red-600 dark:text-red-400" />
          <div>
            <p className="text-sm font-medium text-red-900 dark:text-red-100">
              Failed to load downloaded models
            </p>
            <p className="mt-1 text-xs text-red-700 dark:text-red-300">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  const downloadingTasks = Object.values(activeDownloads).filter(
    (p) => p.status === "downloading" || p.status === "pending"
  );

  if (downloadedModels.length === 0 && downloadingTasks.length === 0) {
    return (
      <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-6 text-center">
        <p className="text-sm text-[var(--muted-foreground)]">
          No models downloaded yet. Download a model from the catalog above.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Active Downloads */}
      {downloadingTasks.map((task) => (
        <div
          key={task.task_id}
          className="rounded-lg border border-blue-500/50 bg-blue-50/50 p-4 dark:border-blue-500/30 dark:bg-blue-500/5"
        >
          <div className="flex items-center justify-between gap-4">
            <div className="flex-1 min-w-0">
              <h3 className="text-sm font-medium text-[var(--foreground)]">
                Downloading {task.task_id}...
              </h3>
              <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-[var(--border)]">
                <div
                  className="h-full bg-blue-500 transition-all duration-300"
                  style={{ width: `${Math.max(0, Math.min(100, task.progress * 100))}%` }}
                />
              </div>
              <div className="mt-1 flex justify-between text-xs text-[var(--muted-foreground)]">
                <span>{Math.round(task.progress * 100)}%</span>
                <span>
                  {task.downloaded_bytes > 0 && task.total_bytes > 0
                    ? `${(task.downloaded_bytes / 1024 / 1024).toFixed(1)} MB / ${(task.total_bytes / 1024 / 1024).toFixed(1)} MB`
                    : "Starting..."}
                </span>
              </div>
            </div>
            <div className="flex shrink-0 items-center">
              <button
                onClick={async () => {
                  try {
                    await cancelDownload(task.task_id);
                    setToast({ message: "Download cancelled", type: "success" });
                  } catch (e) {
                    console.error("Failed to cancel download:", e);
                  }
                }}
                className="inline-flex items-center gap-1.5 rounded-md border border-red-200/60 px-3 py-1.5 text-xs font-medium text-red-600 transition-colors hover:bg-red-50 dark:border-red-900/30 dark:text-red-400 dark:hover:bg-red-900/10"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      ))}
      {toast && (
        <div
          className={`mb-4 rounded-xl p-4 text-sm font-medium ${
            toast.type === "error"
              ? "border border-red-200 bg-red-50 text-red-900 dark:border-red-900/30 dark:bg-red-900/10 dark:text-red-100"
              : "border border-emerald-200 bg-emerald-50 text-emerald-900 dark:border-emerald-900/30 dark:bg-emerald-900/10 dark:text-emerald-100"
          }`}
        >
          {toast.message}
        </div>
      )}
      {downloadedModels.map((model) => {
        const isDeleting = deleting === model.id;
        const isActivating = activating === model.id;

        return (
          <div
            key={model.id}
            className={`rounded-lg border bg-[var(--card)] p-4 transition-colors ${
              model.is_active
                ? "border-emerald-500/50 bg-emerald-50/50 dark:border-emerald-500/30 dark:bg-emerald-500/5"
                : "border-[var(--border)]/60"
            }`}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="font-display text-sm font-medium text-[var(--foreground)]">
                    {model.name}
                  </h3>
                  {model.is_active && (
                    <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600 dark:text-emerald-400" />
                  )}
                </div>
                <div className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-[var(--muted-foreground)]">
                  <span>{model.size_gb} GB</span>
                  <span>·</span>
                  <span>{new Date(model.download_date).toLocaleDateString()}</span>
                </div>
                <p className="mt-1 text-xs text-[var(--muted-foreground)] font-mono">
                  {model.filename}
                </p>
              </div>
              <div className="flex shrink-0 flex-col items-end gap-2">
                {model.is_active ? (
                  <span className="inline-flex items-center gap-1.5 rounded-md border border-emerald-500/50 bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-600 dark:text-emerald-400">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Active
                  </span>
                ) : (
                  <button
                    onClick={() => handleSetActive(model.id)}
                    disabled={isActivating}
                    className="inline-flex items-center gap-1.5 rounded-md border border-[var(--border)]/60 px-3 py-1.5 text-xs font-medium text-[var(--foreground)] transition-colors hover:bg-[var(--muted)] disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isActivating ? (
                      <>
                        <Loader2 className="h-3.5 w-3.5 animate-spin" />
                        Activating...
                      </>
                    ) : (
                      "Set Active"
                    )}
                  </button>
                )}
                <button
                  onClick={() => handleDelete(model.id)}
                  disabled={isDeleting}
                  className="inline-flex items-center gap-1.5 rounded-md border border-red-200/60 px-3 py-1.5 text-xs font-medium text-red-600 transition-colors hover:bg-red-50 dark:border-red-900/30 dark:text-red-400 dark:hover:bg-red-900/10 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isDeleting ? (
                    <>
                      <Loader2 className="h-3.5 w-3.5 animate-spin" />
                      Deleting...
                    </>
                  ) : (
                    <>
                      <Trash2 className="h-3.5 w-3.5" />
                      Delete
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
