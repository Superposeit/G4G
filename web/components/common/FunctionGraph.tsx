"use client";

import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";
import { compileExpr } from "@/lib/graph-spec";
import type { GraphSpec } from "@/lib/graph-spec";

// Fixed categorical palette chosen to stay legible on both light and dark
// surfaces (medium lightness/saturation). Axes, grid and text use theme CSS
// variables so they follow the active theme automatically.
const SERIES_COLORS = [
  "#2563eb", // blue
  "#dc2626", // red
  "#059669", // green
  "#d97706", // amber
  "#7c3aed", // violet
  "#0891b2", // cyan
  "#db2777", // pink
  "#65a30d", // lime
];

const WIDTH = 640;
const HEIGHT = 400;
const PAD = { top: 36, right: 20, bottom: 44, left: 56 };
const PLOT_W = WIDTH - PAD.left - PAD.right;
const PLOT_H = HEIGHT - PAD.top - PAD.bottom;

const DEFAULT_DOMAIN: [number, number] = [-10, 10];
const DEFAULT_SAMPLES = 200;

interface Segment {
  points: Array<[number, number]>;
}

interface Series {
  color: string;
  label?: string;
  segments: Segment[];
}

interface PlotPoint {
  cx: number;
  cy: number;
  label?: string;
}

interface RenderModel {
  x0: number;
  x1: number;
  yMin: number;
  yMax: number;
  xTicks: number[];
  yTicks: number[];
  series: Series[];
  points: PlotPoint[];
  title?: string;
  xLabel?: string;
  yLabel?: string;
  zeroX: number | null;
  zeroY: number | null;
  warnings: string[];
}

function niceStep(range: number, targetCount: number): number {
  if (!(range > 0)) return 1;
  const rough = range / targetCount;
  const pow = Math.pow(10, Math.floor(Math.log10(rough)));
  const norm = rough / pow;
  let mul: number;
  if (norm < 1.5) mul = 1;
  else if (norm < 3) mul = 2;
  else if (norm < 7) mul = 5;
  else mul = 10;
  return mul * pow;
}

function makeTicks(min: number, max: number, targetCount = 8): number[] {
  const step = niceStep(max - min, targetCount);
  if (!(step > 0)) return [min, max];
  const start = Math.ceil(min / step) * step;
  const out: number[] = [];
  const eps = step * 1e-9;
  for (let v = start; v <= max + eps; v += step) {
    out.push(Math.abs(v) < eps ? 0 : v);
  }
  return out.length > 0 ? out : [min, max];
}

function formatTick(value: number): string {
  if (value === 0) return "0";
  const abs = Math.abs(value);
  if (abs >= 1e4 || abs < 1e-3) return value.toExponential(1);
  return String(Math.round(value * 1000) / 1000);
}

function buildModel(spec: GraphSpec): RenderModel {
  const domain =
    spec.domain && spec.domain[0] < spec.domain[1]
      ? spec.domain
      : DEFAULT_DOMAIN;
  const [x0, x1] = domain;
  const samples = Math.max(2, Math.min(spec.samples ?? DEFAULT_SAMPLES, 5000));
  const warnings: string[] = [];

  // Compile + sample each function. Collect finite y for auto-scaling.
  const finiteYs: number[] = [];
  const rawSeries: Array<{
    color: string;
    label?: string;
    sampled: Array<{ x: number; y: number }>;
  }> = [];

  (spec.functions ?? []).forEach((fn, idx) => {
    let compiled: (x: number) => number;
    try {
      compiled = compileExpr(fn.expr);
    } catch (err) {
      warnings.push(`${fn.label ?? fn.expr}: ${(err as Error).message}`);
      return;
    }
    const sampled: Array<{ x: number; y: number }> = [];
    for (let s = 0; s < samples; s += 1) {
      const x = x0 + ((x1 - x0) * s) / (samples - 1);
      let y: number;
      try {
        y = compiled(x);
      } catch {
        y = NaN;
      }
      sampled.push({ x, y });
      if (Number.isFinite(y)) finiteYs.push(y);
    }
    rawSeries.push({
      color: SERIES_COLORS[idx % SERIES_COLORS.length],
      label: fn.label,
      sampled,
    });
  });

  const specPoints = spec.points ?? [];
  for (const pt of specPoints) finiteYs.push(pt.y);

  // Determine y range: explicit `range`, else auto from sampled values.
  let yMin: number;
  let yMax: number;
  if (spec.range && spec.range[0] < spec.range[1]) {
    [yMin, yMax] = spec.range;
  } else if (finiteYs.length > 0) {
    yMin = Math.min(...finiteYs);
    yMax = Math.max(...finiteYs);
    if (yMin === yMax) {
      // Flat line: give it some vertical breathing room.
      const pad = Math.abs(yMin) > 0 ? Math.abs(yMin) * 0.5 : 1;
      yMin -= pad;
      yMax += pad;
    } else {
      const pad = (yMax - yMin) * 0.05;
      yMin -= pad;
      yMax += pad;
    }
  } else {
    // Nothing finite to plot (e.g. all-NaN). Fall back to a neutral window.
    yMin = -1;
    yMax = 1;
  }

  const sx = (x: number) => PAD.left + ((x - x0) / (x1 - x0)) * PLOT_W;
  const sy = (y: number) => PAD.top + (1 - (y - yMin) / (yMax - yMin)) * PLOT_H;

  // Break each function into finite segments (gaps at non-finite y so we never
  // emit NaN coordinates or draw spurious lines across asymptotes).
  const series: Series[] = rawSeries.map((rs) => {
    const segments: Segment[] = [];
    let current: Array<[number, number]> = [];
    for (const { x, y } of rs.sampled) {
      if (Number.isFinite(y)) {
        current.push([sx(x), sy(y)]);
      } else if (current.length > 0) {
        segments.push({ points: current });
        current = [];
      }
    }
    if (current.length > 0) segments.push({ points: current });
    return { color: rs.color, label: rs.label, segments };
  });

  const points: PlotPoint[] = specPoints.map((pt) => ({
    cx: sx(pt.x),
    cy: sy(pt.y),
    label: pt.label,
  }));

  const zeroX = x0 <= 0 && x1 >= 0 ? sx(0) : null;
  const zeroY = yMin <= 0 && yMax >= 0 ? sy(0) : null;

  return {
    x0,
    x1,
    yMin,
    yMax,
    xTicks: makeTicks(x0, x1),
    yTicks: makeTicks(yMin, yMax),
    series,
    points,
    title: spec.title,
    xLabel: spec.xLabel,
    yLabel: spec.yLabel,
    zeroX,
    zeroY,
    warnings,
  };
}

function ErrorBox({ message }: { message: string }) {
  const { t } = useTranslation();
  return (
    <div className="my-4 rounded-xl border border-[var(--border)] bg-[var(--muted)]/40 px-4 py-3 text-sm text-[var(--muted-foreground)]">
      <span className="font-medium text-[var(--foreground)]">
        {t("Graph error:")}{" "}
      </span>
      {message}
    </div>
  );
}

export default function FunctionGraph({ spec }: { spec: GraphSpec }) {
  const { t } = useTranslation();
  const model = useMemo<RenderModel | { error: string }>(() => {
    try {
      return buildModel(spec);
    } catch (err) {
      return { error: (err as Error).message };
    }
  }, [spec]);

  if ("error" in model) {
    return <ErrorBox message={model.error} />;
  }

  const gridColor = "var(--border)";
  const axisColor = "var(--muted-foreground)";
  const labelColor = "var(--muted-foreground)";
  const clipId = "fg-clip";

  const hasLegend = model.series.some((s) => s.label);

  return (
    <figure className="my-4">
      <svg
        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
        width="100%"
        role="img"
        aria-label={model.title ?? "Function graph"}
        preserveAspectRatio="xMidYMid meet"
        style={{ height: "auto", maxWidth: WIDTH, display: "block" }}
        className="rounded-xl border border-[var(--border)] bg-[var(--card)]"
      >
        <defs>
          <clipPath id={clipId}>
            <rect x={PAD.left} y={PAD.top} width={PLOT_W} height={PLOT_H} />
          </clipPath>
        </defs>

        {/* Title */}
        {model.title ? (
          <text
            x={WIDTH / 2}
            y={22}
            textAnchor="middle"
            style={{ fill: "var(--foreground)" }}
            fontSize={15}
            fontWeight={600}
          >
            {model.title}
          </text>
        ) : null}

        {/* Grid, ticks, zero axes and plot border */}
        <GridAndAxes model={model} gridColor={gridColor} axisColor={axisColor} />

        {/* Function polylines */}
        <g clipPath={`url(#${clipId})`}>
          {model.series.map((s, si) =>
            s.segments.map((seg, gi) =>
              seg.points.length === 1 ? (
                <circle
                  key={`${si}-${gi}`}
                  cx={seg.points[0][0]}
                  cy={seg.points[0][1]}
                  r={2}
                  fill={s.color}
                />
              ) : (
                <polyline
                  key={`${si}-${gi}`}
                  points={seg.points.map((p) => `${p[0]},${p[1]}`).join(" ")}
                  fill="none"
                  stroke={s.color}
                  strokeWidth={2}
                  strokeLinejoin="round"
                  strokeLinecap="round"
                />
              ),
            ),
          )}
        </g>

        {/* Explicit points */}
        <g clipPath={`url(#${clipId})`}>
          {model.points.map((pt, i) => (
            <g key={`pt-${i}`}>
              <circle
                cx={pt.cx}
                cy={pt.cy}
                r={3.5}
                style={{ fill: "var(--primary)" }}
                stroke="var(--card)"
                strokeWidth={1}
              />
              {pt.label ? (
                <text
                  x={pt.cx + 6}
                  y={pt.cy - 6}
                  style={{ fill: "var(--foreground)" }}
                  fontSize={11}
                >
                  {pt.label}
                </text>
              ) : null}
            </g>
          ))}
        </g>

        {/* Axis labels */}
        {model.xLabel ? (
          <text
            x={PAD.left + PLOT_W / 2}
            y={HEIGHT - 6}
            textAnchor="middle"
            style={{ fill: labelColor }}
            fontSize={12}
          >
            {model.xLabel}
          </text>
        ) : null}
        {model.yLabel ? (
          <text
            x={14}
            y={PAD.top + PLOT_H / 2}
            textAnchor="middle"
            transform={`rotate(-90 14 ${PAD.top + PLOT_H / 2})`}
            style={{ fill: labelColor }}
            fontSize={12}
          >
            {model.yLabel}
          </text>
        ) : null}

        {/* Legend */}
        {hasLegend ? (
          <g>
            {model.series.map((s, i) =>
              s.label ? (
                <g
                  key={`lg-${i}`}
                  transform={`translate(${PAD.left + 8}, ${PAD.top + 8 + i * 16})`}
                >
                  <rect width={14} height={3} y={4} rx={1.5} fill={s.color} />
                  <text
                    x={20}
                    y={8}
                    style={{ fill: "var(--foreground)" }}
                    fontSize={11}
                  >
                    {s.label}
                  </text>
                </g>
              ) : null,
            )}
          </g>
        ) : null}
      </svg>
      {model.warnings.length > 0 ? (
        <figcaption className="mt-1 text-xs text-[var(--muted-foreground)]">
          {model.warnings.map((w, i) => (
            <div key={i}>{t("Skipped")} {w}</div>
          ))}
        </figcaption>
      ) : null}
    </figure>
  );
}

/**
 * Grid lines, tick labels, plot border and the emphasised zero axes. Uses the
 * exact same linear maps as `buildModel` (derived from the model's domain /
 * y-range) so grid lines stay aligned with the plotted curves.
 */
function GridAndAxes({
  model,
  gridColor,
  axisColor,
}: {
  model: RenderModel;
  gridColor: string;
  axisColor: string;
}) {
  const sx = (x: number) =>
    PAD.left + ((x - model.x0) / (model.x1 - model.x0)) * PLOT_W;
  const sy = (y: number) =>
    PAD.top + (1 - (y - model.yMin) / (model.yMax - model.yMin)) * PLOT_H;

  return (
    <g>
      {/* Vertical grid + x tick labels */}
      {model.xTicks.map((tick, i) => {
        const x = sx(tick);
        return (
          <g key={`x-${i}`}>
            <line
              x1={x}
              y1={PAD.top}
              x2={x}
              y2={PAD.top + PLOT_H}
              stroke={gridColor}
              strokeWidth={1}
              opacity={0.35}
            />
            <text
              x={x}
              y={PAD.top + PLOT_H + 16}
              textAnchor="middle"
              style={{ fill: axisColor }}
              fontSize={11}
            >
              {formatTick(tick)}
            </text>
          </g>
        );
      })}

      {/* Horizontal grid + y tick labels */}
      {model.yTicks.map((tick, i) => {
        const y = sy(tick);
        return (
          <g key={`y-${i}`}>
            <line
              x1={PAD.left}
              y1={y}
              x2={PAD.left + PLOT_W}
              y2={y}
              stroke={gridColor}
              strokeWidth={1}
              opacity={0.35}
            />
            <text
              x={PAD.left - 8}
              y={y + 3.5}
              textAnchor="end"
              style={{ fill: axisColor }}
              fontSize={11}
            >
              {formatTick(tick)}
            </text>
          </g>
        );
      })}

      {/* Emphasised zero axes */}
      {model.zeroY !== null ? (
        <line
          x1={PAD.left}
          y1={model.zeroY}
          x2={PAD.left + PLOT_W}
          y2={model.zeroY}
          stroke={axisColor}
          strokeWidth={1.5}
        />
      ) : null}
      {model.zeroX !== null ? (
        <line
          x1={model.zeroX}
          y1={PAD.top}
          x2={model.zeroX}
          y2={PAD.top + PLOT_H}
          stroke={axisColor}
          strokeWidth={1.5}
        />
      ) : null}

      {/* Plot border */}
      <rect
        x={PAD.left}
        y={PAD.top}
        width={PLOT_W}
        height={PLOT_H}
        fill="none"
        stroke={gridColor}
        strokeWidth={1}
      />
    </g>
  );
}
