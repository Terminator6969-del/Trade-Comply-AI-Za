"use client"

import { cn } from "@/lib/utils"

/* Grouped vertical bar chart — weekly import/export volume */
export function VolumeBarChart({
  data,
}: {
  data: { day: string; imports: number; exports: number }[]
}) {
  const max = Math.max(...data.flatMap((d) => [d.imports, d.exports]), 1)
  return (
    <div>
      <div className="flex items-end gap-3">
        {data.map((d) => (
          <div key={d.day} className="flex flex-1 flex-col items-center gap-2">
            <div className="flex h-40 w-full items-end justify-center gap-1">
              <div
                className="w-3 rounded-t-md bg-primary transition-all"
                style={{ height: `${Math.max((d.imports / max) * 100, 4)}%` }}
                title={`${d.imports} imports`}
              />
              <div
                className="w-3 rounded-t-md bg-primary/25 transition-all"
                style={{ height: `${Math.max((d.exports / max) * 100, 4)}%` }}
                title={`${d.exports} exports`}
              />
            </div>
            <span className="text-xs font-medium text-muted-foreground">{d.day}</span>
          </div>
        ))}
      </div>
      <div className="mt-4 flex items-center gap-4 text-xs text-muted-foreground">
        <span className="flex items-center gap-1.5">
          <span className="size-2.5 rounded-sm bg-primary" /> Imports
        </span>
        <span className="flex items-center gap-1.5">
          <span className="size-2.5 rounded-sm bg-primary/25" /> Exports
        </span>
      </div>
    </div>
  )
}

/* Donut / gauge — compliance rate */
export function ComplianceGauge({ value }: { value: number }) {
  const r = 70
  const circ = Math.PI * r // half circle
  const offset = circ - (value / 100) * circ
  return (
    <div className="flex flex-col items-center">
      <div className="relative">
        <svg width="200" height="120" viewBox="0 0 200 120">
          <path
            d="M 20 110 A 80 80 0 0 1 180 110"
            fill="none"
            stroke="var(--muted)"
            strokeWidth="16"
            strokeLinecap="round"
          />
          <path
            d="M 20 110 A 80 80 0 0 1 180 110"
            fill="none"
            stroke="var(--primary)"
            strokeWidth="16"
            strokeLinecap="round"
            strokeDasharray={circ * (80 / r)}
            strokeDashoffset={(offset * 80) / r}
          />
        </svg>
        <div className="absolute inset-x-0 bottom-1 flex flex-col items-center">
          <span className="text-3xl font-bold text-foreground">{value}%</span>
          <span className="text-xs text-muted-foreground">Compliance rate</span>
        </div>
      </div>
    </div>
  )
}

/* Line / area chart — risk trend */
export function RiskTrendChart({
  data,
}: {
  data: { month: string; score: number }[]
}) {
  const w = 520
  const h = 180
  const pad = 28
  const max = 100
  const min = 60
  const stepX = (w - pad * 2) / (data.length - 1)
  const points = data.map((d, i) => {
    const x = pad + i * stepX
    const y = h - pad - ((d.score - min) / (max - min)) * (h - pad * 2)
    return { x, y, ...d }
  })
  const linePath = points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ")
  const areaPath = `${linePath} L ${points[points.length - 1].x} ${h - pad} L ${points[0].x} ${h - pad} Z`

  return (
    <div className="w-full overflow-x-auto">
      <svg viewBox={`0 0 ${w} ${h}`} className="w-full" role="img" aria-label="Risk trend chart">
        <defs>
          <linearGradient id="riskFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="var(--primary)" stopOpacity="0.25" />
            <stop offset="100%" stopColor="var(--primary)" stopOpacity="0" />
          </linearGradient>
        </defs>
        {[0, 0.5, 1].map((g) => (
          <line
            key={g}
            x1={pad}
            x2={w - pad}
            y1={pad + g * (h - pad * 2)}
            y2={pad + g * (h - pad * 2)}
            stroke="var(--border)"
            strokeDasharray="4 4"
          />
        ))}
        <path d={areaPath} fill="url(#riskFill)" />
        <path d={linePath} fill="none" stroke="var(--primary)" strokeWidth="2.5" strokeLinecap="round" />
        {points.map((p) => (
          <g key={p.month}>
            <circle cx={p.x} cy={p.y} r="4" fill="var(--primary)" stroke="var(--card)" strokeWidth="2" />
            <text x={p.x} y={h - 8} textAnchor="middle" className="fill-muted-foreground text-[10px]">
              {p.month}
            </text>
          </g>
        ))}
      </svg>
    </div>
  )
}

/* Horizontal progress bar */
export function MiniBar({ value, className }: { value: number; className?: string }) {
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
      <div
        className={cn("h-full rounded-full bg-primary", className)}
        style={{ width: `${Math.min(value, 100)}%` }}
      />
    </div>
  )
}