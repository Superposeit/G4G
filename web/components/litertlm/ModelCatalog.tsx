"use client";

import { useEffect, useState, useCallback } from "react";
import {
  Download,
  CheckCircle2,
  AlertTriangle,
  Info,
  Loader2,
  Search,
  ArrowDownWideNarrow,
  Heart,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import {
  getAvailableModels,
  getDownloadedModels,
  downloadModel,
  getDownloadProgress,
  type ModelWithCompatibility,
  type DownloadedModelInfo,
  type DownloadProgress,
} from "@/lib/litertlm-api";

export default function ModelCatalog() {
  const { t } = useTranslation();
  const [availableModels, setAvailableModels] = useState<ModelWithCompatibility[] | null>(null);
  const [downloadedModels, setDownloadedModels] = useState<DownloadedModelInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [toast, setToast] = useState<{ message: string; type: "error" | "success" } | null>(null);
  const [activeDownloads, setActiveDownloads] = useState<Record<string, DownloadProgress>>({});

  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(null), 5000);
    return () => clearTimeout(timer);
  }, [toast]);

  const fetchModels = useCallback(async (search = "") => {
    try {
      const [available, downloaded] = await Promise.all([
        getAvailableModels(search),
        getDownloadedModels(),
      ]);
      setAvailableModels(available);
      setDownloadedModels(downloaded);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load models");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchModels();
  }, [fetchModels]);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const progress = await getDownloadProgress();
        setActiveDownloads(progress);
      } catch (e) {
        // ignore
      }
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchInput !== searchQuery) {
        setSearchQuery(searchInput);
        setLoading(true);
        fetchModels(searchInput);
      }
    }, 400);
    return () => clearTimeout(timer);
  }, [searchInput, searchQuery, fetchModels]);

  const handleDownload = async (modelId: string) => {
    setDownloading(modelId);
    try {
      await downloadModel(modelId);
      const downloaded = await getDownloadedModels();
      setDownloadedModels(downloaded);
      setToast({ message: "Download started successfully.", type: "success" });
    } catch (e) {
      console.error("Failed to download model:", e);
      setToast({
        message: e instanceof Error ? e.message : "Failed to download model",
        type: "error",
      });
    } finally {
      setDownloading(null);
    }
  };

  const isDownloaded = (modelId: string) => {
    return downloadedModels.some((m) => m.id === modelId);
  };

  const formatNumber = (n: number) => {
    if (n >= 1000) return `${(n / 1000).toFixed(1)}k`;
    return String(n);
  };

  return (
    <div className="space-y-4">
      {toast && (
        <div
          className={`rounded-xl p-4 text-sm font-medium ${
            toast.type === "error"
              ? "border border-red-200 bg-red-50 text-red-900 dark:border-red-900/30 dark:bg-red-900/10 dark:text-red-100"
              : "border border-emerald-200 bg-emerald-50 text-emerald-900 dark:border-emerald-900/30 dark:bg-emerald-900/10 dark:text-emerald-100"
          }`}
        >
          {toast.message}
        </div>
      )}

      {/* Search bar */}
      <div className="relative">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted-foreground)]" />
        <input
          type="text"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder="Search litert-community models..."
          className="w-full rounded-lg border border-[var(--border)]/60 bg-[var(--card)] py-2.5 pl-9 pr-3 text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] outline-none transition-colors focus:border-[var(--foreground)]/30"
        />
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-6 w-6 animate-spin text-[var(--muted-foreground)]" />
        </div>
      ) : error ? (
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
      ) : !availableModels || availableModels.length === 0 ? (
        <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-6 text-center">
          <p className="text-sm text-[var(--muted-foreground)]">
            {searchInput ? "No models match your search" : "No models available"}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          <p className="text-xs text-[var(--muted-foreground)]">
            {availableModels.length} model{availableModels.length !== 1 ? "s" : ""} from{" "}
            <span className="font-medium">litert-community</span>
          </p>
          {availableModels.map(({ model, compatibility }) => {
            const downloaded = isDownloaded(model.id);
            const activeTask = activeDownloads[model.id];
            const isDownloading = downloading === model.id || (activeTask && (activeTask.status === "pending" || activeTask.status === "downloading"));

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
                    <div className="mt-2 flex flex-wrap items-center gap-3">
                      {model.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1.5">
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
                      {/* Stats */}
                      <div className="flex items-center gap-3 text-[10px] text-[var(--muted-foreground)]">
                        <span className="inline-flex items-center gap-1">
                          <ArrowDownWideNarrow className="h-3 w-3" />
                          {formatNumber(model.downloads)}
                        </span>
                        <span className="inline-flex items-center gap-1">
                          <Heart className="h-3 w-3" />
                          {formatNumber(model.likes)}
                        </span>
                      </div>
                    </div>
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
      )}
    </div>
  );
}
