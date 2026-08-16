import { ArrowDownRight, ArrowUpRight } from "lucide-react";
import { motion } from "framer-motion";
import { Area, AreaChart, ResponsiveContainer } from "recharts";
import { kpiSparklines } from "../lib/data";
import { CountUp } from "./ui";
import { clsx } from "../lib/format";

const cards = [
  {
    key: "shipments",
    label: "Active shipments",
    value: 186,
    suffix: "",
    delta: 8.4,
    hint: "vs last 30 days",
    accent: true,
    data: kpiSparklines.shipments,
    color: "#B7EE55",
  },
  {
    key: "compliance",
    label: "Compliance rate",
    value: 96.4,
    suffix: "%",
    decimals: 1,
    delta: 1.6,
    hint: "first-pass SARS",
    accent: false,
    data: kpiSparklines.compliance,
    color: "#0F2B24",
  },
  {
    key: "duties",
    label: "Duties assessed",
    value: 18.4,
    prefix: "R ",
    suffix: "m",
    decimals: 1,
    delta: 4.2,
    hint: "ZAR this month",
    accent: false,
    data: kpiSparklines.duties,
    color: "#0F2B24",
  },
  {
    key: "actions",
    label: "Items requiring action",
    value: 14,
    suffix: "",
    delta: -12.5,
    hint: "open exceptions",
    accent: false,
    invert: true,
    data: kpiSparklines.actions,
    color: "#c2410c",
  },
];

export function KpiCards() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map((c, i) => {
        const up = c.delta >= 0;
        const good = c.invert ? !up : up;
        return (
          <motion.div
            key={c.key}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 * i, duration: 0.4 }}
            className={clsx(
              "card-hover relative overflow-hidden rounded-2xl border p-5",
              c.accent
                ? "border-transparent bg-[#0F2B24] text-white shadow-[0_12px_32px_rgba(15,43,36,0.22)]"
                : "border-[#e6eae2]/90 bg-white/88 backdrop-blur-sm dark:border-white/8 dark:bg-[#102820]/72",
            )}
          >
            {c.accent && (
              <span className="pointer-events-none absolute -right-8 -top-10 h-32 w-32 rounded-full bg-[#A3E635]/25 blur-2xl" />
            )}
            <div className="flex items-start justify-between">
              <p
                className={clsx(
                  "text-[13px] font-medium",
                  c.accent ? "text-white/70" : "text-[#6b7a72]",
                )}
              >
                {c.label}
              </p>
              <span
                className={clsx(
                  "flex h-7 w-7 items-center justify-center rounded-full",
                  c.accent
                    ? "bg-white/10 text-[#B7EE55]"
                    : good
                      ? "bg-emerald-50 text-emerald-600 dark:bg-emerald-400/10 dark:text-emerald-300"
                      : "bg-rose-50 text-rose-600 dark:bg-rose-400/10 dark:text-rose-300",
                )}
              >
                {up ? <ArrowUpRight className="h-3.5 w-3.5" /> : <ArrowDownRight className="h-3.5 w-3.5" />}
              </span>
            </div>
            <p className={clsx("mt-3 text-[34px] font-semibold leading-none tracking-tight", c.accent ? "text-white" : "text-[#12211c] dark:text-white")}>
              <CountUp
                value={c.value}
                decimals={"decimals" in c ? (c.decimals as number) : 0}
                prefix={"prefix" in c ? (c.prefix as string) : ""}
                suffix={c.suffix}
              />
            </p>
            <div className="mt-3 flex items-end justify-between gap-3">
              <p className={clsx("text-[11.5px]", c.accent ? "text-[#B7EE55]" : good ? "text-emerald-600 dark:text-emerald-300" : "text-rose-600")}>
                {up ? "+" : ""}
                {c.delta}% <span className={c.accent ? "text-white/50" : "text-[#8a968e]"}>{c.hint}</span>
              </p>
              <div className="h-8 w-24">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={c.data.map((v, idx) => ({ i: idx, v }))}>
                    <defs>
                      <linearGradient id={`spark-${c.key}`} x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor={c.accent ? "#B7EE55" : c.color} stopOpacity={0.45} />
                        <stop offset="100%" stopColor={c.accent ? "#B7EE55" : c.color} stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <Area
                      type="monotone"
                      dataKey="v"
                      stroke={c.accent ? "#B7EE55" : c.color}
                      strokeWidth={1.6}
                      fill={`url(#spark-${c.key})`}
                      dot={false}
                      isAnimationActive
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
