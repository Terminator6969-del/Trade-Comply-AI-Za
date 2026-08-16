import { clsx } from "../lib/format";
import type { Risk, Status } from "../lib/types";
import { useEffect, useState } from "react";

export function Card({
  children,
  className = "",
  padded = true,
}: {
  children: React.ReactNode;
  className?: string;
  padded?: boolean;
}) {
  return (
    <div
      className={clsx(
        "card-hover rounded-2xl border border-[#e6eae2]/90 bg-white/90 shadow-[0_1px_2px_rgba(15,43,36,0.035),0_8px_24px_rgba(15,43,36,0.04)] backdrop-blur-sm dark:border-white/8 dark:bg-[#102820]/72 dark:shadow-[0_8px_28px_rgba(0,0,0,0.25)]",
        padded && "p-5",
        className,
      )}
    >
      {children}
    </div>
  );
}

export function StatusPill({ status }: { status: Status }) {
  const map: Record<Status, string> = {
    cleared: "bg-emerald-50 text-emerald-700 ring-emerald-100 dark:bg-emerald-400/10 dark:text-emerald-300 dark:ring-emerald-400/15",
    in_review: "bg-amber-50 text-amber-700 ring-amber-100 dark:bg-amber-400/10 dark:text-amber-300 dark:ring-amber-400/15",
    held: "bg-rose-50 text-rose-700 ring-rose-100 dark:bg-rose-400/10 dark:text-rose-300 dark:ring-rose-400/15",
    in_transit: "bg-sky-50 text-sky-700 ring-sky-100 dark:bg-sky-400/10 dark:text-sky-300 dark:ring-sky-400/15",
    draft: "bg-stone-100 text-stone-600 ring-stone-200 dark:bg-white/8 dark:text-stone-300 dark:ring-white/10",
  };
  const label: Record<Status, string> = {
    cleared: "Cleared",
    in_review: "In review",
    held: "Held",
    in_transit: "In transit",
    draft: "Draft",
  };
  return (
    <span className={clsx("inline-flex items-center rounded-full px-2.5 py-0.5 text-[11px] font-semibold ring-1", map[status])}>
      {label[status]}
    </span>
  );
}

export function RiskBadge({ risk }: { risk: Risk }) {
  const map: Record<Risk, string> = {
    low: "bg-[#0F2B24] text-[#B7EE55]",
    medium: "bg-amber-100 text-amber-800 dark:bg-amber-400/15 dark:text-amber-200",
    high: "bg-rose-100 text-rose-700 dark:bg-rose-400/15 dark:text-rose-200",
  };
  return (
    <span className={clsx("inline-flex items-center rounded-md px-2 py-0.5 text-[11px] font-semibold capitalize tracking-wide", map[risk])}>
      {risk}
    </span>
  );
}

export function CountUp({
  value,
  duration = 900,
  decimals = 0,
  prefix = "",
  suffix = "",
}: {
  value: number;
  duration?: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
}) {
  const [n, setN] = useState(0);
  useEffect(() => {
    let raf = 0;
    const start = performance.now();
    const tick = (t: number) => {
      const p = Math.min(1, (t - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setN(value * eased);
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [value, duration]);
  return (
    <span className="tabular">
      {prefix}
      {n.toLocaleString("en-ZA", {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
      })}
      {suffix}
    </span>
  );
}

export function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[#8a968e] dark:text-[#7d8c84]">
      {children}
    </p>
  );
}

export function Empty({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-[#d7ddd4] px-6 py-12 text-center dark:border-white/10">
      <p className="text-sm font-semibold text-[#12211c] dark:text-white">{title}</p>
      <p className="mt-1 text-sm text-[#6b7a72]">{body}</p>
    </div>
  );
}
