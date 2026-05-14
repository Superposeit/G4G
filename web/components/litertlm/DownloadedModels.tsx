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
  type DownloadedModelInfo,
} from "@/lib/litertlm-api";

export default function DownloadedModels() {
  const { t } = useTranslation();
  const [downloadedModels, setDownloadedModels] = useState<DownloadedModelInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);
  const [activating, setActivating] = useState<string | null>(null);
  const [toast, setToast] = useState<{ message: string; type: "error" | "success" } | null>(null);

  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(null), 5000);
    return () => clearTimeout(timer);
  }, [toast]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await getDownloadedModels();
        if (!cancelled) {
          setDownloadedModels(data);
          setLoading(false);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load downloaded models");
          setLoading(false);
        }
      }
    })();
    return () => {
      cancelled = true;
    };
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

  if (downloadedModels.length === 0) {
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
                  <h3 className="text-sm font-medium text-[var(--foreground)]">
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
