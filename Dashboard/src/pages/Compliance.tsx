import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { actionQueue } from "../lib/data";
import { reports, rulesCatalog } from "../lib/ops";
import { Card, RiskBadge } from "../components/ui";
import { ComplianceChart, InsightsCard } from "../components/Charts";
import { ShieldAlert, ShieldCheck } from "lucide-react";
import { clsx, formatDate } from "../lib/format";

const controls = [
  { name: "SARS first-pass rate", value: "96.4%", status: "Healthy", note: "Above 94% SLA" },
  { name: "ITAC permit coverage", value: "91%", status: "Watch", note: "3 lines expire this week" },
  { name: "Origin claim accuracy", value: "98.6%", status: "Healthy", note: "SADC + EPA" },
  { name: "Document completeness", value: "88%", status: "Action", note: "Aspen + Clover packs" },
  { name: "Denied-party screening", value: "100%", status: "Healthy", note: "OFAC / EU / UN" },
  { name: "AEO trusted trader", value: "Active", status: "Healthy", note: "Renewal Nov 2026" },
];

export function Compliance() {
  const [risk, setRisk] = useState("all");
  const [rule, setRule] = useState("all");
  const rows = useMemo(
    () => reports.filter((r) => (risk === "all" || r.risk === risk) && (rule === "all" || r.rule === rule)),
    [risk, rule],
  );
  return (
    <div className="space-y-5">
      <div>
        <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-[#8a968e]">Governance</p>
        <h1 className="mt-1 text-[28px] font-semibold tracking-tight">Compliance</h1>
        <p className="mt-1 text-[13.5px] text-[#6b7a72]">
          Control tower for SARS, ITAC, SAHPRA, NRCS and preference-origin obligations.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3">
        {controls.map((c) => (
          <Card key={c.name}>
            <div className="flex items-start justify-between">
              <p className="text-[13px] text-[#6b7a72]">{c.name}</p>
              {c.status === "Healthy" ? (
                <ShieldCheck className="h-4 w-4 text-emerald-600" />
              ) : (
                <ShieldAlert className="h-4 w-4 text-amber-600" />
              )}
            </div>
            <p className="mt-2 text-[24px] font-semibold">{c.value}</p>
            <p className="mt-1 text-[12px] text-[#8a968e]">{c.note}</p>
            <span
              className={clsx(
                "mt-3 inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold",
                c.status === "Healthy" && "bg-emerald-50 text-emerald-700 dark:bg-emerald-400/10 dark:text-emerald-300",
                c.status === "Watch" && "bg-amber-50 text-amber-700 dark:bg-amber-400/10 dark:text-amber-300",
                c.status === "Action" && "bg-rose-50 text-rose-700 dark:bg-rose-400/10 dark:text-rose-300",
              )}
            >
              {c.status}
            </span>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-3 xl:grid-cols-12">
        <div className="xl:col-span-7">
          <ComplianceChart />
        </div>
        <div className="xl:col-span-5">
          <InsightsCard />
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        <select value={risk} onChange={(e) => setRisk(e.target.value)} className="h-10 rounded-full border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5">
          <option value="all">All risk</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <select value={rule} onChange={(e) => setRule(e.target.value)} className="h-10 rounded-full border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5">
          <option value="all">All rule codes</option>
          {rulesCatalog.map((r) => (
            <option key={r.code} value={r.code}>{r.code}</option>
          ))}
        </select>
      </div>

      <Card padded={false} className="overflow-hidden">
        <div className="px-5 py-4">
          <h3 className="text-[15px] font-semibold">Compliance reports</h3>
          <p className="text-[12px] text-[#6b7a72]">{rows.length} scored entries</p>
        </div>
        <table className="w-full min-w-[720px] text-left text-[13px]">
          <thead>
            <tr className="border-y border-[#eef1ea] text-[11px] font-semibold uppercase tracking-[0.12em] text-[#8a968e] dark:border-white/8">
              <th className="px-5 py-3">Report</th>
              <th className="px-5 py-3">Shipment</th>
              <th className="px-5 py-3">Score</th>
              <th className="px-5 py-3">Risk</th>
              <th className="px-5 py-3">Rule</th>
              <th className="px-5 py-3">Date</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id} className="border-b border-[#f3f5f0] dark:border-white/5">
                <td className="px-5 py-3 font-mono text-[12px] font-semibold">{r.id}</td>
                <td className="px-5 py-3">
                  <Link to={`/shipments/${r.shipmentId}`} className="font-medium text-[#0F2B24] dark:text-[#B7EE55]">{r.company}</Link>
                  <p className="font-mono text-[11px] text-[#8a968e]">{r.shipmentId}</p>
                </td>
                <td className="px-5 py-3 tabular font-semibold">{r.score}</td>
                <td className="px-5 py-3"><RiskBadge risk={r.risk} /></td>
                <td className="px-5 py-3 font-mono text-[12px]">{r.rule}</td>
                <td className="px-5 py-3 text-[#6b7a72]">{formatDate(r.date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      <Card>
        <h3 className="text-[15px] font-semibold">Exception queue</h3>
        <ul className="mt-3 divide-y divide-[#eef1ea] dark:divide-white/8">
          {actionQueue.map((a) => (
            <li key={a.id} className="flex items-center justify-between py-3">
              <div>
                <p className="text-[13px] font-semibold">{a.label}</p>
                <p className="font-mono text-[11px] text-[#8a968e]">{a.id}</p>
              </div>
              <span
                className={clsx(
                  "rounded-full px-2.5 py-0.5 text-[11px] font-semibold",
                  a.tone === "red" && "bg-rose-50 text-rose-700",
                  a.tone === "amber" && "bg-amber-50 text-amber-700",
                  a.tone === "blue" && "bg-sky-50 text-sky-700",
                )}
              >
                {a.due}
              </span>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
