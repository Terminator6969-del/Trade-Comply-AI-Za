import {
  Area,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Line,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { complianceSeries, insights, laneSeries, riskDistribution } from "../lib/data";
import { Card } from "./ui";
import { ArrowUpRight, Sparkles } from "lucide-react";
import { clsx } from "../lib/format";
import { useApp } from "../lib/store";

function TipShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-[#e4e8e2] bg-white/95 px-3 py-2 text-[12px] shadow-lg backdrop-blur dark:border-white/10 dark:bg-[#122821]/95">
      {children}
    </div>
  );
}

function ComplianceTip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{ dataKey?: string; value?: number; color?: string }>;
  label?: string;
}) {
  if (!active || !payload?.length) return null;
  const rate = payload.find((p) => p.dataKey === "rate");
  const vol = payload.find((p) => p.dataKey === "volume");
  return (
    <TipShell>
      <p className="mb-1 font-semibold text-[#12211c] dark:text-white">{label}</p>
      {rate && (
        <p className="text-[#0F2B24] dark:text-[#B7EE55]">
          Compliance <span className="tabular font-semibold">{rate.value?.toFixed(1)}%</span>
        </p>
      )}
      {vol && (
        <p className="text-[#6b7a72]">
          Volume <span className="tabular font-semibold">{vol.value} shipments</span>
        </p>
      )}
    </TipShell>
  );
}

function BarTip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{ dataKey?: string; value?: number }>;
  label?: string;
}) {
  if (!active || !payload?.length) return null;
  return (
    <TipShell>
      <p className="mb-1 font-semibold text-[#12211c] dark:text-white">{label} lane</p>
      {payload.map((p) => (
        <p key={p.dataKey} className="capitalize text-[#6b7a72]">
          {p.dataKey === "cleared" ? "Cleared" : "In review"}{" "}
          <span className="tabular font-semibold text-[#12211c] dark:text-white">{p.value}</span>
        </p>
      ))}
    </TipShell>
  );
}

export function ComplianceChart() {
  const dark = useApp((s) => s.dark);
  const axis = dark ? "#7d8c84" : "#8a968e";
  const grid = dark ? "rgba(255,255,255,0.06)" : "#eef1ea";
  return (
    <Card className="h-full">
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <h3 className="text-[15px] font-semibold text-[#12211c] dark:text-white">Compliance rate over time</h3>
          <p className="mt-0.5 text-[12px] text-[#6b7a72]">First-pass SARS clearance vs weekly shipment volume</p>
        </div>
        <div className="flex items-center gap-3 text-[11px] text-[#6b7a72]">
          <span className="inline-flex items-center gap-1.5">
            <span className="h-1.5 w-4 rounded-full bg-[#0F2B24] dark:bg-[#A3E635]" />
            Rate
          </span>
          <span className="inline-flex items-center gap-1.5">
            <span className="h-px w-4 border-t border-dashed border-[#8a968e]" />
            Volume
          </span>
        </div>
      </div>
      <div className="h-[280px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={complianceSeries} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}>
            <defs>
              <linearGradient id="rateFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#0F2B24" stopOpacity={dark ? 0.45 : 0.22} />
                <stop offset="100%" stopColor="#A3E635" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke={grid} vertical={false} />
            <XAxis dataKey="week" tick={{ fill: axis, fontSize: 11 }} axisLine={false} tickLine={false} />
            <YAxis
              yAxisId="left"
              domain={[88, 100]}
              tick={{ fill: axis, fontSize: 11 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v) => `${v}%`}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              domain={[80, 220]}
              tick={{ fill: axis, fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip content={<ComplianceTip />} />
            <Area
              yAxisId="left"
              type="monotone"
              dataKey="rate"
              stroke={dark ? "#A3E635" : "#0F2B24"}
              strokeWidth={2.2}
              fill="url(#rateFill)"
              animationDuration={900}
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="volume"
              stroke="#8a968e"
              strokeDasharray="5 5"
              strokeWidth={1.6}
              dot={false}
              animationDuration={1100}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

export function RiskDonut() {
  const total = riskDistribution.reduce((a, b) => a + b.value, 0);
  return (
    <Card className="h-full">
      <h3 className="text-[15px] font-semibold text-[#12211c] dark:text-white">Risk distribution</h3>
      <p className="mt-0.5 text-[12px] text-[#6b7a72]">Active consignments by AI risk score</p>
      <div className="relative mx-auto mt-2 h-[210px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={riskDistribution}
              dataKey="value"
              nameKey="name"
              innerRadius={62}
              outerRadius={88}
              paddingAngle={3}
              stroke="none"
              animationDuration={800}
            >
              {riskDistribution.map((d) => (
                <Cell key={d.name} fill={d.color} />
              ))}
            </Pie>
            <Tooltip
              content={({ active, payload }) => {
                if (!active || !payload?.[0]) return null;
                const p = payload[0].payload as { name: string; value: number };
                return (
                  <TipShell>
                    <p className="font-semibold text-[#12211c] dark:text-white">
                      {p.name} risk · {p.value}
                    </p>
                    <p className="text-[#6b7a72]">{((p.value / total) * 100).toFixed(1)}% of book</p>
                  </TipShell>
                );
              }}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
          <p className="text-[28px] font-semibold leading-none text-[#12211c] dark:text-white tabular">{total}</p>
          <p className="mt-1 text-[11px] text-[#6b7a72]">shipments</p>
        </div>
      </div>
      <ul className="mt-1 space-y-1.5">
        {riskDistribution.map((d) => (
          <li key={d.name} className="flex items-center justify-between text-[12.5px]">
            <span className="inline-flex items-center gap-2 text-[#5c6b64] dark:text-[#c5d0c8]">
              <span className="h-2 w-2 rounded-full" style={{ background: d.color }} />
              {d.name}
            </span>
            <span className="tabular font-semibold text-[#12211c] dark:text-white">{d.value}</span>
          </li>
        ))}
      </ul>
    </Card>
  );
}

export function LaneBars() {
  const dark = useApp((s) => s.dark);
  const axis = dark ? "#7d8c84" : "#8a968e";
  return (
    <Card className="h-full">
      <h3 className="text-[15px] font-semibold text-[#12211c] dark:text-white">Shipments by trade lane</h3>
      <p className="mt-0.5 text-[12px] text-[#6b7a72]">Cleared vs still in review · last 30 days</p>
      <div className="mt-3 h-[230px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={laneSeries} barGap={4} margin={{ top: 8, right: 4, left: -22, bottom: 0 }}>
            <CartesianGrid stroke={dark ? "rgba(255,255,255,0.06)" : "#eef1ea"} vertical={false} />
            <XAxis dataKey="lane" tick={{ fill: axis, fontSize: 11 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: axis, fontSize: 11 }} axisLine={false} tickLine={false} />
            <Tooltip content={<BarTip />} cursor={{ fill: dark ? "rgba(255,255,255,0.04)" : "rgba(15,43,36,0.04)" }} />
            <Bar dataKey="cleared" stackId="a" fill="#0F2B24" radius={[0, 0, 0, 0]} barSize={28} />
            <Bar dataKey="review" stackId="a" fill="#A3E635" radius={[8, 8, 0, 0]} barSize={28} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-1 flex gap-4 text-[11px] text-[#6b7a72]">
        <span className="inline-flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-sm bg-[#0F2B24]" /> Cleared
        </span>
        <span className="inline-flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-sm bg-[#A3E635]" /> In review
        </span>
      </div>
    </Card>
  );
}

export function InsightsCard() {
  const tone: Record<string, string> = {
    amber: "bg-amber-50 text-amber-700 dark:bg-amber-400/10 dark:text-amber-200",
    green: "bg-emerald-50 text-emerald-700 dark:bg-emerald-400/10 dark:text-emerald-200",
    blue: "bg-sky-50 text-sky-700 dark:bg-sky-400/10 dark:text-sky-200",
  };
  const bar: Record<string, string> = {
    amber: "bg-amber-400",
    green: "bg-emerald-500",
    blue: "bg-sky-500",
  };
  return (
    <Card className="h-full">
      <div className="mb-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#0F2B24] text-[#B7EE55]">
            <Sparkles className="h-3.5 w-3.5" />
          </span>
          <h3 className="text-[15px] font-semibold text-[#12211c] dark:text-white">AI insights</h3>
        </div>
        <span className="text-[11px] font-medium text-[#8a968e]">Updated 4m ago</span>
      </div>
      <ul className="space-y-2.5">
        {insights.map((ins) => (
          <li
            key={ins.id}
            className="relative overflow-hidden rounded-xl border border-[#eef1ea] bg-[#fbfcf9] p-3 dark:border-white/8 dark:bg-white/4"
          >
            <span className={clsx("absolute bottom-3 left-0 top-3 w-1 rounded-r-full", bar[ins.tone])} />
            <div className="pl-2">
              <div className="flex items-start justify-between gap-2">
                <p className="text-[13px] font-semibold text-[#12211c] dark:text-white">{ins.title}</p>
                <span className={clsx("shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold", tone[ins.tone])}>
                  {ins.tone === "amber" ? "Action" : ins.tone === "green" ? "Saving" : "Watch"}
                </span>
              </div>
              <p className="mt-1 text-[12px] leading-relaxed text-[#6b7a72]">{ins.body}</p>
              <button className="mt-2 inline-flex items-center gap-0.5 text-[12px] font-semibold text-[#0F2B24] dark:text-[#B7EE55]">
                {ins.action}
                <ArrowUpRight className="h-3.5 w-3.5" />
              </button>
            </div>
          </li>
        ))}
      </ul>
    </Card>
  );
}
