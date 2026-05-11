"use client";

import { useEffect, useState } from "react";
import {
  Download,
  CheckCircle2,
  AlertTriangle,
  Info,
  Loader2,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import {
  getAvailableModels,
  getDownloadedModels,
  downloadModel,
  type ModelWithCompatibility,
  type DownloadedModelInfo,
} from "@/lib/litertlm-api";

export default function ModelCatalog() {
  const { t } = useTranslation();
  const [availableModels, setAvailableModels] = useState<ModelWithCompatibility[] | null>(null);
  const [downloadedModels, setDownloadedModels] = useState<DownloadedModelInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [available, downloaded] = await Promise.all([
          getAvailableModels(),
          getDownloadedModels(),
        ]);
        if (!cancelled) {
          setAvailableModels(available);
          setDownloadedModels(downloaded);
          setLoading(false);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load models");
          setLoading(false);
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const handleDownload = async (modelId: string) => {
    setDownloading(modelId);
    try {
      await downloadModel(modelId);
      // Refresh downloaded models
      const downloaded = await getDownloadedModels();
      setDownloadedModels(downloaded);
    } catch (e) {
      console.error("Failed to download model:", e);
      alert(e instanceof Error ? e.message : "Failed to download model");
    } finally {
      setDownloading(null);
    }
  };

  const isDownloaded = (modelId: string) => {
    return downloadedModels.some((m) => m.id === modelId);
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
              Failed to load models
            </p>
            <p className="mt-1 text-xs text-red-700 dark:text-red-300">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!availableModels || availableModels.length === 0) {
    return (
      <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-6 text-center">
        <p className="text-sm text-[var(--muted-foreground)]">No models available</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {availableModels.map(({ model, compatibility }) => {
        const downloaded = isDownloaded(model.id);
        const isDownloading = downloading === model.id;

        return (
          <div
            key={model.id}
            className="rounded-lg border border-[var(--border)]/60 bg-[var(--card)] p-4 transition-colors hover:border-[var(--border)]"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-medium text-[var(--foreground)]">
                    {model.name}
                  </h3>
                  {downloaded && (
                    <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600 dark:text-emerald-400" />
                  )}
                </div>
                <p className="mt-1 text-xs text-[var(--muted-foreground)]">
                  {model.description}
                </p>
                <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-[var(--muted-foreground)]">
                  <span>{model.size_gb} GB</span>
                  <span>·</span>
                  <span>{model.ram_gb} GB RAM required</span>
                  <span>·</span>
                  <span>{model.context_window} context window</span>
                </div>
                {model.tags.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {model.tags.map((tag) => (
                      <span
                        key={tag}
                        className="rounded-full border border-[var(--border)]/60 px-2 py-0.5 text-[10px] text-[var(--muted-foreground)]"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <div className="flex shrink-0 flex-col items-end gap-2">
                {/* Compatibility status */}
                {!compatibility.compatible && compatibility.issues.length > 0 && (
                  <div className="flex items-start gap-1.5 text-xs text-red-600 dark:text-red-400">
                    <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                    <span className="text-right">
                      {compatibility.issues[0]}
                    </span>
                  </div>
                )}
                {compatibility.compatible && compatibility.warnings.length > 0 && (
                  <div className="flex items-start gap-1.5 text-xs text-amber-600 dark:text-amber-400">
                    <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                    <span className="text-right">
                      {compatibility.warnings[0]}
                    </span>
                  </div>
                )}
                {/* Download button */}
                {downloaded ? (
                  <button
                    disabled
                    className="inline-flex items-center gap-1.5 rounded-md border border-[var(--border)]/60 px-3 py-1.5 text-xs font-medium text-[var(--muted-foreground)] opacity-60"
                  >
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Downloaded
                  </button>
                ) : (
                  <button
                    onClick={() => handleDownload(model.id)}
                    disabled={isDownloading || !compatibility.compatible}
                    className="inline-flex items-center gap-1.5 rounded-md bg-[var(--foreground)] px-3 py-1.5 text-xs font-medium text-[var(--background)] transition-opacity hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isDownloading ? (
                      <>
                        <Loader2 className="h-3.5 w-3.5 animate-spin" />
                        Downloading...
                      </>
                    ) : (
                      <>
                        <Download className="h-3.5 w-3.5" />
                        Download
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
