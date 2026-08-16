import { Link, useParams } from "react-router-dom";
import { useMemo, useState } from "react";
import { ArrowLeft, CheckCircle2, FileText, Play, RefreshCw, ShieldAlert } from "lucide-react";
import { useApp } from "../lib/store";
import { formatDate, formatZar, clsx } from "../lib/format";
import { Card, RiskBadge, StatusPill } from "../components/ui";
import { auditLog, incoterms, lineItems, rulesFor } from "../lib/ops";
import { useRunCompliance } from "../lib/api";

const tabs = ["Overview", "Compliance", "Documents", "Line items", "Audit log"] as const;
type Tab = (typeof tabs)[number];

export function ShipmentDetail() {
  const { id } = useParams();
  const shipments = useApp((s) => s.shipments);
  const documents = useApp((s) => s.documents);
  const s = shipments.find((x) => x.id === id);
  const [tab, setTab] = useState<Tab>("Overview");
  const run = useRunCompliance();

  if (!s) {
    return (
      <div className="py-20 text-center">
        <p className="text-lg font-semibold">Shipment not found</p>
        <Link to="/shipments" className="mt-3 inline-block text-sm font-semibold text-[#0F2B24] dark:text-[#B7EE55]">
          Back to shipments
        </Link>
      </div>
    );
  }

  const docs = documents.filter((d) => d.shipmentId === s.id);
  const rules = rulesFor(s.id);
  const events = auditLog.filter((a) => a.shipmentId === s.id);
  const term = incoterms[s.id] ?? "CIF Cape Town";
  const vat = Math.round((s.value + s.duty) * 0.15);

  return (
    <div className="space-y-5">
      <Link
        to="/shipments"
        className="inline-flex items-center gap-1.5 text-[13px] font-medium text-[#6b7a72] hover:text-[#0F2B24]"
      >
        <ArrowLeft className="h-4 w-4" /> All shipments
      </Link>
      <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="font-mono text-[12px] font-semibold text-[#8a968e]">{s.sarsRef} · {term} · ZAR</p>
          <h1 className="mt-1 font-mono text-[28px] font-semibold tracking-tight text-[#0F2B24] dark:text-[#B7EE55]">
            {s.id}
          </h1>
          <p className="mt-1 text-[14px] text-[#5c6b64] dark:text-[#c5d0c8]">
            {s.company} · {s.origin} → {s.destination}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <StatusPill status={s.status} />
          <RiskBadge risk={s.risk} />
          <button
            onClick={() => run.mutate(s.id)}
            disabled={run.isPending}
            className="inline-flex h-10 items-center gap-2 rounded-full bg-[#0F2B24] px-4 text-[13px] font-semibold text-white dark:bg-[#A3E635] dark:text-[#0F2B24]"
          >
            {run.isPending ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
            Run compliance
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {[
          { label: "Customs value", value: formatZar(s.value) },
          { label: "Duty assessed", value: formatZar(s.duty) },
          { label: "HS heading", value: s.hsCode },
          { label: "Incoterms", value: term },
        ].map((k) => (
          <Card key={k.label}>
            <p className="text-[12px] text-[#6b7a72]">{k.label}</p>
            <p className="mt-1 tabular text-[20px] font-semibold text-[#12211c] dark:text-white">{k.value}</p>
          </Card>
        ))}
      </div>

      <div className="flex gap-1 overflow-x-auto rounded-full bg-white/70 p-1 ring-1 ring-[#e6eae2] dark:bg-white/5 dark:ring-white/8">
        {tabs.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={clsx(
              "whitespace-nowrap rounded-full px-4 py-1.5 text-[13px] font-semibold transition",
              tab === t
                ? "bg-[#0F2B24] text-white dark:bg-[#A3E635] dark:text-[#0F2B24]"
                : "text-[#5c6b64] hover:bg-white dark:text-[#c5d0c8]",
            )}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "Overview" && (
        <div className="grid grid-cols-1 gap-3 lg:grid-cols-3">
          <Card className="lg:col-span-2">
            <h3 className="text-[15px] font-semibold">Entry details</h3>
            <dl className="mt-4 grid grid-cols-1 gap-x-8 gap-y-3 sm:grid-cols-2">
              {[
                ["Consignee", s.consignee],
                ["Broker", s.broker],
                ["Trade lane", s.lane],
                ["Flow", s.flow],
                ["Declared", formatDate(s.date)],
                ["ETA", formatDate(s.eta)],
                ["Gross weight", `${s.weight.toLocaleString("en-ZA")} kg`],
                ["Containers", String(s.containers)],
                ["Classification", `${s.hsCode} — ${s.hsDesc}`],
                ["Documents", `${docs.length} lodged`],
              ].map(([k, v]) => (
                <div key={k}>
                  <dt className="text-[11px] font-semibold uppercase tracking-wider text-[#8a968e]">{k}</dt>
                  <dd className="mt-0.5 text-[13.5px] font-medium">{v}</dd>
                </div>
              ))}
            </dl>
            <div className="mt-5 rounded-xl bg-[#f4f6f0] p-4 text-[13px] leading-relaxed text-[#3d4d46] dark:bg-white/5 dark:text-[#d5ddd6]">
              {s.notes}
            </div>
          </Card>
          <Card>
            <h3 className="text-[15px] font-semibold">Duty worksheet</h3>
            <div className="mt-3 space-y-1.5 text-[13px]">
              <div className="flex justify-between"><span className="text-[#6b7a72]">Customs value</span><span className="tabular font-medium">{formatZar(s.value)}</span></div>
              <div className="flex justify-between"><span className="text-[#6b7a72]">Duty</span><span className="tabular font-medium">{formatZar(s.duty)}</span></div>
              <div className="flex justify-between"><span className="text-[#6b7a72]">VAT 15%</span><span className="tabular font-medium">{formatZar(vat)}</span></div>
              <div className="mt-2 flex justify-between border-t border-[#eef1ea] pt-2 font-semibold dark:border-white/8">
                <span>Payable</span>
                <span className="tabular">{formatZar(s.duty + vat)}</span>
              </div>
            </div>
          </Card>
        </div>
      )}

      {tab === "Compliance" && (
        <Card>
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-[15px] font-semibold">Rule report</h3>
              <p className="text-[12px] text-[#6b7a72]">SARS · ITAC · SAHPRA · NRCS · origin</p>
            </div>
            <span className="text-[12px] text-[#8a968e]">{rules.length} checks</span>
          </div>
          <ul className="space-y-2">
            {rules.map((r) => (
              <RuleRow key={r.code} code={r.code} title={r.title} severity={r.severity} body={r.body} source={r.source} />
            ))}
          </ul>
        </Card>
      )}

      {tab === "Documents" && (
        <Card padded={false} className="overflow-hidden">
          <table className="w-full min-w-[640px] text-left text-[13px]">
            <thead>
              <tr className="border-b border-[#eef1ea] text-[11px] font-semibold uppercase tracking-[0.12em] text-[#8a968e] dark:border-white/8">
                <th className="px-5 py-3">ID</th>
                <th className="px-5 py-3">Type</th>
                <th className="px-5 py-3">Status</th>
                <th className="px-5 py-3">Updated</th>
                <th className="px-5 py-3">Size</th>
              </tr>
            </thead>
            <tbody>
              {docs.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-5 py-10 text-center text-[#6b7a72]">No documents lodged.</td>
                </tr>
              )}
              {docs.map((d) => (
                <tr key={d.id} className="border-b border-[#f3f5f0] dark:border-white/5">
                  <td className="px-5 py-3 font-mono text-[12px] font-semibold">{d.id}</td>
                  <td className="px-5 py-3">{d.type}</td>
                  <td className="px-5 py-3 capitalize">{d.status}</td>
                  <td className="px-5 py-3 text-[#6b7a72]">{formatDate(d.updated)}</td>
                  <td className="px-5 py-3 text-[#6b7a72]">{d.size}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}

      {tab === "Line items" && (
        <LineItemsTable shipmentId={s.id} fallbackHs={s.hsCode} fallbackDesc={s.hsDesc} value={s.value} />
      )}

      {tab === "Audit log" && (
        <Card>
          <h3 className="text-[15px] font-semibold">Audit trail</h3>
          <ol className="mt-4 space-y-3">
            {(events.length
              ? events
              : [{ id: "x", actor: "System", action: "Draft created", time: s.date, detail: "Entry opened in Cape Town Hub." }]
            ).map((e) => (
              <li key={e.id} className="flex gap-3">
                <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-[#A3E635]" />
                <div>
                  <p className="text-[13px] font-semibold">
                    {e.action} <span className="font-normal text-[#8a968e]">· {e.actor}</span>
                  </p>
                  <p className="text-[12px] text-[#6b7a72]">{e.detail}</p>
                  <p className="mt-0.5 font-mono text-[11px] text-[#9aa59d]">{e.time}</p>
                </div>
              </li>
            ))}
          </ol>
        </Card>
      )}
    </div>
  );
}

function RuleRow({
  code, title, severity, body, source,
}: {
  code: string; title: string; severity: "pass" | "warn" | "fail" | "info"; body: string; source: string;
}) {
  const [open, setOpen] = useState(false);
  const tone = {
    pass: "bg-emerald-50 text-emerald-700 dark:bg-emerald-400/10 dark:text-emerald-300",
    warn: "bg-amber-50 text-amber-700 dark:bg-amber-400/10 dark:text-amber-300",
    fail: "bg-rose-50 text-rose-700 dark:bg-rose-400/10 dark:text-rose-300",
    info: "bg-sky-50 text-sky-700 dark:bg-sky-400/10 dark:text-sky-300",
  }[severity];
  return (
    <li className="rounded-xl border border-[#eef1ea] dark:border-white/8">
      <button onClick={() => setOpen((v) => !v)} className="flex w-full items-center gap-3 px-4 py-3 text-left">
        {severity === "fail" ? <ShieldAlert className="h-4 w-4 text-rose-600" /> : <CheckCircle2 className="h-4 w-4 text-emerald-600" />}
        <span className="flex-1">
          <span className="block text-[13px] font-semibold">{title}</span>
          <span className="font-mono text-[11px] text-[#8a968e]">{code}</span>
        </span>
        <span className={clsx("rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase", tone)}>{severity}</span>
      </button>
      {open && (
        <div className="border-t border-[#eef1ea] px-4 py-3 text-[13px] text-[#5c6b64] dark:border-white/8 dark:text-[#c5d0c8]">
          <p>{body}</p>
          <p className="mt-1 text-[11px] text-[#8a968e]">Source · {source}</p>
        </div>
      )}
    </li>
  );
}

function LineItemsTable({
  shipmentId, fallbackHs, fallbackDesc, value,
}: {
  shipmentId: string; fallbackHs: string; fallbackDesc: string; value: number;
}) {
  const seed = useMemo(() => {
    const found = lineItems.filter((l) => l.shipmentId === shipmentId);
    if (found.length) return found.map((l) => ({ ...l }));
    return [{
      id: "LI-X", shipmentId, sku: "LINE-01", description: fallbackDesc,
      hsSuggested: fallbackHs, hsConfirmed: fallbackHs, confidence: 0.86,
      qty: 1, unit: "lot", value, origin: "ZA",
    }];
  }, [shipmentId, fallbackHs, fallbackDesc, value]);
  const [rows, setRows] = useState(seed);

  return (
    <Card padded={false} className="overflow-hidden">
      <div className="flex items-center justify-between px-5 py-4">
        <div>
          <h3 className="text-[15px] font-semibold">Line items</h3>
          <p className="text-[12px] text-[#6b7a72]">Suggested HS can be confirmed inline.</p>
        </div>
        <FileText className="h-4 w-4 text-[#8a968e]" />
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[860px] text-left text-[13px]">
          <thead>
            <tr className="border-y border-[#eef1ea] text-[11px] font-semibold uppercase tracking-[0.12em] text-[#8a968e] dark:border-white/8">
              <th className="px-5 py-3">SKU</th>
              <th className="px-5 py-3">Description</th>
              <th className="px-5 py-3">HS suggested</th>
              <th className="px-5 py-3">HS confirmed</th>
              <th className="px-5 py-3">Conf.</th>
              <th className="px-5 py-3">Qty</th>
              <th className="px-5 py-3 text-right">Value</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((l, i) => (
              <tr key={l.id} className="border-b border-[#f3f5f0] dark:border-white/5">
                <td className="px-5 py-3 font-mono text-[12px]">{l.sku}</td>
                <td className="px-5 py-3">{l.description}</td>
                <td className="px-5 py-3 font-mono text-[12px] text-[#8a968e]">{l.hsSuggested}</td>
                <td className="px-5 py-3">
                  <input
                    value={l.hsConfirmed}
                    onChange={(e) => setRows((prev) => prev.map((r, idx) => (idx === i ? { ...r, hsConfirmed: e.target.value } : r)))}
                    className="h-8 w-24 rounded-lg border border-[#e2e7de] bg-white px-2 font-mono text-[12px] dark:border-white/10 dark:bg-white/5"
                  />
                </td>
                <td className="px-5 py-3">
                  <span className={clsx(
                    "rounded-full px-2 py-0.5 text-[11px] font-semibold",
                    l.confidence >= 0.85 ? "bg-emerald-50 text-emerald-700" : l.confidence >= 0.7 ? "bg-amber-50 text-amber-700" : "bg-rose-50 text-rose-700",
                  )}>
                    {Math.round(l.confidence * 100)}%
                  </span>
                </td>
                <td className="px-5 py-3 tabular">{l.qty.toLocaleString("en-ZA")} {l.unit}</td>
                <td className="px-5 py-3 text-right tabular font-semibold">{formatZar(l.value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
