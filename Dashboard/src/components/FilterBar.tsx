import { CalendarRange } from "lucide-react";
import { useApp } from "../lib/store";
import { clsx } from "../lib/format";
import type { DateRange, TradeFlow } from "../lib/types";

const ranges: { id: DateRange; label: string }[] = [
  { id: "7d", label: "7 days" },
  { id: "30d", label: "30 days" },
  { id: "90d", label: "90 days" },
  { id: "ytd", label: "YTD" },
];

const flows: { id: TradeFlow; label: string }[] = [
  { id: "all", label: "All flows" },
  { id: "import", label: "Import" },
  { id: "export", label: "Export" },
];

export function FilterBar() {
  const { dateRange, setDateRange, tradeFlow, setTradeFlow } = useApp();
  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-[#e6eae2]/90 bg-white/75 px-3.5 py-2.5 shadow-sm backdrop-blur-xl dark:border-white/8 dark:bg-[#102820]/60 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-2 text-[12.5px] text-[#6b7a72]">
        <span className="pulse-dot h-2 w-2 rounded-full bg-[#A3E635]" />
        <CalendarRange className="h-4 w-4" />
        <span className="font-medium">Live filters</span>
        <span className="hidden text-[#b0b8b2] sm:inline">·</span>
        <span className="hidden sm:inline">Cape Town · Durban · Johannesburg</span>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <div className="flex rounded-full bg-[#eef1ea] p-0.5 dark:bg-white/8">
          {ranges.map((r) => (
            <button
              key={r.id}
              onClick={() => setDateRange(r.id)}
              className={clsx(
                "rounded-full px-3 py-1 text-[12px] font-semibold transition",
                dateRange === r.id
                  ? "bg-[#0F2B24] text-white dark:bg-[#A3E635] dark:text-[#0F2B24]"
                  : "text-[#5c6b64] hover:text-[#0F2B24] dark:text-[#c5d0c8]",
              )}
            >
              {r.label}
            </button>
          ))}
        </div>
        <div className="flex rounded-full bg-[#eef1ea] p-0.5 dark:bg-white/8">
          {flows.map((f) => (
            <button
              key={f.id}
              onClick={() => setTradeFlow(f.id)}
              className={clsx(
                "rounded-full px-3 py-1 text-[12px] font-semibold transition",
                tradeFlow === f.id
                  ? "bg-white text-[#0F2B24] shadow-sm dark:bg-[#0F2B24] dark:text-[#B7EE55]"
                  : "text-[#5c6b64] dark:text-[#c5d0c8]",
              )}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
