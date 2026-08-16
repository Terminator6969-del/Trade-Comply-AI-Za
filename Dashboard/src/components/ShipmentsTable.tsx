import { ArrowRight, ArrowUpDown, ChevronLeft, ChevronRight } from "lucide-react";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { formatDate, formatZar, clsx } from "../lib/format";
import { useApp } from "../lib/store";
import type { Risk, Status } from "../lib/types";
import { Card, RiskBadge, StatusPill } from "./ui";

type SortKey = "id" | "company" | "status" | "risk" | "value" | "date";

export function ShipmentsTable({ compact = false }: { compact?: boolean }) {
  const { shipments, tradeFlow, query } = useApp();
  const nav = useNavigate();
  const [status, setStatus] = useState<Status | "all">("all");
  const [risk, setRisk] = useState<Risk | "all">("all");
  const [sort, setSort] = useState<{ key: SortKey; dir: "asc" | "desc" }>({ key: "date", dir: "desc" });
  const [page, setPage] = useState(0);
  const [size, setSize] = useState(compact ? 6 : 10);

  const rows = useMemo(() => {
    let list = shipments.filter((s) => {
      if (tradeFlow !== "all" && s.flow !== tradeFlow) return false;
      if (status !== "all" && s.status !== status) return false;
      if (risk !== "all" && s.risk !== risk) return false;
      if (query.trim()) {
        const q = query.toLowerCase();
        return (
          s.id.toLowerCase().includes(q) ||
          s.company.toLowerCase().includes(q) ||
          s.origin.toLowerCase().includes(q) ||
          s.destination.toLowerCase().includes(q) ||
          s.hsCode.includes(q)
        );
      }
      return true;
    });
    list = [...list].sort((a, b) => {
      const dir = sort.dir === "asc" ? 1 : -1;
      const av = a[sort.key];
      const bv = b[sort.key];
      if (typeof av === "number" && typeof bv === "number") return (av - bv) * dir;
      return String(av).localeCompare(String(bv)) * dir;
    });
    return list;
  }, [shipments, tradeFlow, query, status, risk, sort]);

  const pages = Math.max(1, Math.ceil(rows.length / size));
  const slice = rows.slice(page * size, page * size + size);

  const toggle = (key: SortKey) => {
    setSort((s) => (s.key === key ? { key, dir: s.dir === "asc" ? "desc" : "asc" } : { key, dir: "asc" }));
  };

  return (
    <Card padded={false} className="overflow-hidden">
      <div className="flex flex-col gap-3 border-b border-[#eef1ea] px-5 py-4 dark:border-white/8 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h3 className="text-[15px] font-semibold text-[#12211c] dark:text-white">Recent shipments</h3>
          <p className="text-[12px] text-[#6b7a72]">{rows.length} matching SARS entries</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value as Status | "all");
              setPage(0);
            }}
            className="h-9 rounded-full border border-[#e2e7de] bg-white px-3 text-[12px] dark:border-white/10 dark:bg-white/5 dark:text-white"
          >
            <option value="all">All statuses</option>
            <option value="cleared">Cleared</option>
            <option value="in_review">In review</option>
            <option value="held">Held</option>
            <option value="in_transit">In transit</option>
            <option value="draft">Draft</option>
          </select>
          <select
            value={risk}
            onChange={(e) => {
              setRisk(e.target.value as Risk | "all");
              setPage(0);
            }}
            className="h-9 rounded-full border border-[#e2e7de] bg-white px-3 text-[12px] dark:border-white/10 dark:bg-white/5 dark:text-white"
          >
            <option value="all">All risk</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[760px] text-left">
          <thead>
            <tr className="border-b border-[#eef1ea] text-[11px] font-semibold uppercase tracking-[0.12em] text-[#8a968e] dark:border-white/8">
              {(
                [
                  ["id", "Reference"],
                  ["company", "Company / route"],
                  ["status", "Status"],
                  ["risk", "Risk"],
                  ["value", "Customs value"],
                  ["date", "Date"],
                ] as [SortKey, string][]
              ).map(([key, label]) => (
                <th key={key} className="px-5 py-3 font-semibold">
                  <button onClick={() => toggle(key)} className="inline-flex items-center gap-1 hover:text-[#0F2B24] dark:hover:text-white">
                    {label}
                    <ArrowUpDown className="h-3 w-3" />
                  </button>
                </th>
              ))}
              <th className="px-5 py-3" />
            </tr>
          </thead>
          <tbody>
            {slice.map((s) => (
              <tr
                key={s.id}
                onClick={() => nav(`/shipments/${s.id}`)}
                className="cursor-pointer border-b border-[#f3f5f0] transition hover:bg-[#f7faf3] dark:border-white/5 dark:hover:bg-white/4"
              >
                <td className="px-5 py-3.5 font-mono text-[12.5px] font-semibold text-[#0F2B24] dark:text-[#B7EE55]">
                  {s.id}
                </td>
                <td className="px-5 py-3.5">
                  <p className="text-[13px] font-semibold text-[#12211c] dark:text-white">{s.company}</p>
                  <p className="text-[11.5px] text-[#6b7a72]">
                    {s.origin} → {s.destination}
                  </p>
                </td>
                <td className="px-5 py-3.5">
                  <StatusPill status={s.status} />
                </td>
                <td className="px-5 py-3.5">
                  <RiskBadge risk={s.risk} />
                </td>
                <td className="px-5 py-3.5 text-right tabular text-[13px] font-semibold text-[#12211c] dark:text-white">
                  {formatZar(s.value)}
                </td>
                <td className="px-5 py-3.5 text-[12.5px] text-[#5c6b64] dark:text-[#c5d0c8]">{formatDate(s.date)}</td>
                <td className="px-5 py-3.5">
                  <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[#f0f3eb] text-[#0F2B24] dark:bg-white/8 dark:text-[#B7EE55]">
                    <ArrowRight className="h-4 w-4" />
                  </span>
                </td>
              </tr>
            ))}
            {slice.length === 0 && (
              <tr>
                <td colSpan={7} className="px-5 py-12 text-center text-sm text-[#6b7a72]">
                  No shipments match the current filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="flex flex-col gap-3 px-5 py-3.5 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2 text-[12px] text-[#6b7a72]">
          Rows
          {[10, 25, 50].map((n) => (
            <button
              key={n}
              onClick={() => {
                setSize(n);
                setPage(0);
              }}
              className={clsx(
                "h-7 min-w-7 rounded-full px-2 font-semibold",
                size === n ? "bg-[#0F2B24] text-white dark:bg-[#A3E635] dark:text-[#0F2B24]" : "hover:bg-[#eef1ea] dark:hover:bg-white/8",
              )}
            >
              {n}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 text-[12px] text-[#6b7a72]">
          <span>
            {rows.length === 0 ? 0 : page * size + 1}–{Math.min(rows.length, (page + 1) * size)} of {rows.length}
          </span>
          <button
            disabled={page === 0}
            onClick={() => setPage((p) => p - 1)}
            className="rounded-full p-1.5 disabled:opacity-30 hover:bg-[#eef1ea] dark:hover:bg-white/8"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <button
            disabled={page >= pages - 1}
            onClick={() => setPage((p) => p + 1)}
            className="rounded-full p-1.5 disabled:opacity-30 hover:bg-[#eef1ea] dark:hover:bg-white/8"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </Card>
  );
}
