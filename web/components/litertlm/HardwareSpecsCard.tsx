"use client";

import { useEffect, useState } from "react";
import {
  Cpu,
  HardDrive,
  MemoryStick,
  Monitor,
  AlertTriangle,
  CheckCircle2,
  Info,
} from "lucide-react";
import { getHardwareSpecs, type HardwareSpecs } from "@/lib/litertlm-api";

export default function HardwareSpecsCard() {
  const [hardware, setHardware] = useState<HardwareSpecs | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await getHardwareSpecs();
        if (!cancelled) {
          setHardware(data);
          setLoading(false);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load hardware specs");
          setLoading(false);
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return (
      <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-6">
        <div className="flex items-center gap-2 text-[var(--muted-foreground)]">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-[var(--border)] border-t-[var(--foreground)]" />
          <span className="text-sm">Loading hardware specs...</span>
        </div>
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
              Failed to load hardware specs
            </p>
            <p className="mt-1 text-xs text-red-700 dark:text-red-300">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!hardware) return null;

  const ramPercent = (hardware.ram_available_gb / hardware.ram_total_gb) * 100;
  const diskPercent = (hardware.disk_available_gb / hardware.disk_total_gb) * 100;

  const ramStatus = ramPercent < 20 ? "critical" : ramPercent < 40 ? "warning" : "ok";
  const diskStatus = diskPercent < 20 ? "critical" : diskPercent < 40 ? "warning" : "ok";

  const statusColor = {
    critical: "text-red-600 dark:text-red-400",
    warning: "text-amber-600 dark:text-amber-400",
    ok: "text-emerald-600 dark:text-emerald-400",
  };

  const statusIcon = {
    critical: AlertTriangle,
    warning: Info,
    ok: CheckCircle2,
  };

  const RamIcon = statusIcon[ramStatus];
  const DiskIcon = statusIcon[diskStatus];

  return (
    <div className="space-y-4">
      {/* CPU */}
      <div className="flex items-start gap-3 rounded-lg border border-[var(--border)]/60 bg-[var(--card)] p-4">
        <Cpu className="mt-0.5 h-5 w-5 shrink-0 text-[var(--muted-foreground)]" />
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-[var(--foreground)]">CPU</p>
          <p className="mt-1 text-xs text-[var(--muted-foreground)]">
            {hardware.cpu_model}
          </p>
          <p className="mt-0.5 text-xs text-[var(--muted-foreground)]">
            {hardware.cpu_cores} cores · {hardware.architecture}
          </p>
        </div>
      </div>

      {/* RAM */}
      <div className="flex items-start gap-3 rounded-lg border border-[var(--border)]/60 bg-[var(--card)] p-4">
        <MemoryStick className="mt-0.5 h-5 w-5 shrink-0 text-[var(--muted-foreground)]" />
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium text-[var(--foreground)]">RAM</p>
            <RamIcon className={`h-4 w-4 ${statusColor[ramStatus]}`} />
          </div>
          <p className="mt-1 text-xs text-[var(--muted-foreground)]">
            {hardware.ram_available_gb.toFixed(1)} GB available of{" "}
            {hardware.ram_total_gb.toFixed(1)} GB total
          </p>
          <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-[var(--border)]">
            <div
              className={`h-full rounded-full transition-all ${
                ramStatus === "critical"
                  ? "bg-red-500"
                  : ramStatus === "warning"
                    ? "bg-amber-500"
                    : "bg-emerald-500"
              }`}
              style={{ width: `${ramPercent}%` }}
            />
          </div>
        </div>
      </div>

      {/* GPU */}
      {hardware.gpu_model && (
        <div className="flex items-start gap-3 rounded-lg border border-[var(--border)]/60 bg-[var(--card)] p-4">
          <Monitor className="mt-0.5 h-5 w-5 shrink-0 text-[var(--muted-foreground)]" />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-[var(--foreground)]">GPU</p>
            <p className="mt-1 text-xs text-[var(--muted-foreground)]">
              {hardware.gpu_model}
            </p>
            {hardware.gpu_memory_gb && (
              <p className="mt-0.5 text-xs text-[var(--muted-foreground)]">
                {hardware.gpu_memory_gb.toFixed(1)} GB VRAM
              </p>
            )}
          </div>
        </div>
      )}

      {/* Disk */}
      <div className="flex items-start gap-3 rounded-lg border border-[var(--border)]/60 bg-[var(--card)] p-4">
        <HardDrive className="mt-0.5 h-5 w-5 shrink-0 text-[var(--muted-foreground)]" />
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium text-[var(--foreground)]">Disk Space</p>
            <DiskIcon className={`h-4 w-4 ${statusColor[diskStatus]}`} />
          </div>
          <p className="mt-1 text-xs text-[var(--muted-foreground)]">
            {hardware.disk_available_gb.toFixed(1)} GB available of{" "}
            {hardware.disk_total_gb.toFixed(1)} GB total
          </p>
          <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-[var(--border)]">
            <div
              className={`h-full rounded-full transition-all ${
                diskStatus === "critical"
                  ? "bg-red-500"
                  : diskStatus === "warning"
                    ? "bg-amber-500"
                    : "bg-emerald-500"
              }`}
              style={{ width: `${diskPercent}%` }}
            />
          </div>
        </div>
      </div>

      {/* Platform */}
      <div className="flex items-center gap-2 text-xs text-[var(--muted-foreground)]">
        <span>{hardware.platform}</span>
        <span>·</span>
        <span>{hardware.architecture}</span>
      </div>
    </div>
  );
}
