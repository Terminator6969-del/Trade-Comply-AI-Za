import { clsx } from "../lib/format";

export function Skeleton({ className = "" }: { className?: string }) {
  return <div className={clsx("animate-pulse rounded-xl bg-[#e6eae2] dark:bg-white/8", className)} />;
}

export function TableSkeleton({ rows = 6 }: { rows?: number }) {
  return (
    <div className="space-y-2 p-5">
      {Array.from({ length: rows }).map((_, i) => (
        <Skeleton key={i} className="h-11 w-full" />
      ))}
    </div>
  );
}

export function KpiSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <Skeleton key={i} className="h-[132px] rounded-2xl" />
      ))}
    </div>
  );
}
