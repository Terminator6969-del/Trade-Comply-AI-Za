import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { FileUp, RefreshCw, X } from "lucide-react";
import { formatDate, clsx } from "../lib/format";
import { Card } from "../components/ui";
import { useApp } from "../lib/store";
import { useUploadDocument } from "../lib/api";
import type { DocumentRow } from "../lib/types";

const tones: Record<string, string> = {
  verified: "bg-emerald-50 text-emerald-700 dark:bg-emerald-400/10 dark:text-emerald-300",
  pending: "bg-amber-50 text-amber-700 dark:bg-amber-400/10 dark:text-amber-300",
  rejected: "bg-rose-50 text-rose-700 dark:bg-rose-400/10 dark:text-rose-300",
  expired: "bg-stone-100 text-stone-600 dark:bg-white/8 dark:text-stone-300",
  processing: "bg-sky-50 text-sky-700 dark:bg-sky-400/10 dark:text-sky-300",
  failed: "bg-rose-50 text-rose-700 dark:bg-rose-400/10 dark:text-rose-300",
};

function extractOf(d: DocumentRow) {
  if (d.extraction) return d.extraction;
  if (d.status === "verified") return "completed";
  if (d.status === "pending") return "pending";
  if (d.status === "processing") return "processing";
  return "failed";
}

export function Documents() {
  const documents = useApp((s) => s.documents);
  const updateDocument = useApp((s) => s.updateDocument);
  const upload = useUploadDocument();
  const [q, setQ] = useState("");
  const [status, setStatus] = useState("all");
  const [active, setActive] = useState<DocumentRow | null>(null);
  const [drag, setDrag] = useState(false);
  const rows = useMemo(
    () =>
      documents.filter((d) => {
        if (status !== "all" && d.status !== status) return false;
        const hay = `${d.id} ${d.type} ${d.shipmentId} ${d.party} ${d.filename ?? ""}`.toLowerCase();
        return hay.includes(q.toLowerCase());
      }),
    [documents, q, status],
  );

  const onFiles = (files: FileList | null) => {
    if (!files?.[0]) return;
    const f = files[0];
    if (f.size > 10 * 1024 * 1024) {
      useApp.getState().setToast("Max file size is 10MB.");
      window.setTimeout(() => useApp.getState().setToast(null), 2400);
      return;
    }
    upload.mutate(f);
  };

  const reextract = (d: DocumentRow) => {
    updateDocument(d.id, { status: "processing", extraction: "processing" });
    window.setTimeout(() => {
      updateDocument(d.id, {
        status: "verified",
        extraction: "completed",
        confidence: 0.9,
        fields: [
          { label: "Document type", value: d.type, confidence: 0.94 },
          { label: "Shipment", value: d.shipmentId, confidence: 0.9 },
          { label: "Party", value: d.party, confidence: 0.87 },
        ],
      });
      useApp.getState().setToast("Re-extraction complete.");
      window.setTimeout(() => useApp.getState().setToast(null), 2200);
    }, 1100);
  };

  return (
    <div className="space-y-5">
      <div>
        <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-[#8a968e]">Control</p>
        <h1 className="mt-1 text-[28px] font-semibold tracking-tight">Documents</h1>
        <p className="mt-1 text-[13.5px] text-[#6b7a72]">SAD500s, permits and origin packs. PDF, JPG or PNG · 10MB max.</p>
      </div>

      <label
        onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={(e) => { e.preventDefault(); setDrag(false); onFiles(e.dataTransfer.files); }}
        className={clsx(
          "flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed px-6 py-10 text-center transition",
          drag ? "border-[#A3E635] bg-[#f4fbe6]" : "border-[#d5dccf] bg-white/70 dark:border-white/15 dark:bg-white/4",
        )}
      >
        <FileUp className="h-6 w-6 text-[#0F2B24] dark:text-[#B7EE55]" />
        <p className="mt-2 text-[14px] font-semibold">Drop files or click to upload</p>
        <p className="mt-1 text-[12px] text-[#6b7a72]">Commercial invoices extract first. AI fills SAD500 lines.</p>
        <input type="file" accept=".pdf,.jpg,.jpeg,.png" className="hidden" onChange={(e) => onFiles(e.target.files)} />
      </label>

      <div className="flex flex-wrap gap-2">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search documents…"
          className="h-10 w-64 rounded-full border border-[#e2e7de] bg-white px-4 text-[13px] dark:border-white/10 dark:bg-white/5"
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="h-10 rounded-full border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5"
        >
          <option value="all">All statuses</option>
          <option value="verified">Verified</option>
          <option value="pending">Pending</option>
          <option value="processing">Processing</option>
          <option value="rejected">Rejected</option>
          <option value="failed">Failed</option>
          <option value="expired">Expired</option>
        </select>
      </div>
      <Card padded={false} className="overflow-hidden">
        <table className="w-full min-w-[700px] text-left text-[13px]">
          <thead>
            <tr className="border-b border-[#eef1ea] text-[11px] font-semibold uppercase tracking-[0.12em] text-[#8a968e] dark:border-white/8">
              <th className="px-5 py-3">ID</th>
              <th className="px-5 py-3">Type</th>
              <th className="px-5 py-3">Shipment</th>
              <th className="px-5 py-3">Extraction</th>
              <th className="px-5 py-3">Status</th>
              <th className="px-5 py-3">Updated</th>
              <th className="px-5 py-3" />
            </tr>
          </thead>
          <tbody>
            {rows.map((d) => (
              <tr
                key={d.id}
                onClick={() => setActive(d)}
                className="cursor-pointer border-b border-[#f3f5f0] hover:bg-[#f7faf3] dark:border-white/5 dark:hover:bg-white/4"
              >
                <td className="px-5 py-3 font-mono text-[12px] font-semibold">{d.id}</td>
                <td className="px-5 py-3 font-medium">{d.type}</td>
                <td className="px-5 py-3">
                  <Link to={`/shipments/${d.shipmentId}`} onClick={(e) => e.stopPropagation()} className="font-mono text-[12px] text-[#0F2B24] dark:text-[#B7EE55]">
                    {d.shipmentId}
                  </Link>
                </td>
                <td className="px-5 py-3 capitalize text-[#6b7a72]">{extractOf(d)}</td>
                <td className="px-5 py-3">
                  <span className={`rounded-full px-2 py-0.5 text-[11px] font-semibold capitalize ${tones[d.status]}`}>
                    {d.status}
                  </span>
                </td>
                <td className="px-5 py-3 text-[#6b7a72]">{formatDate(d.updated)}</td>
                <td className="px-5 py-3">
                  {(d.status === "failed" || d.status === "rejected") && (
                    <button
                      onClick={(e) => { e.stopPropagation(); reextract(d); }}
                      className="inline-flex items-center gap-1 text-[12px] font-semibold text-[#0F2B24] dark:text-[#B7EE55]"
                    >
                      <RefreshCw className="h-3.5 w-3.5" /> Re-extract
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      {active && (
        <div className="fixed inset-0 z-50 flex justify-end bg-[#0F2B24]/25 backdrop-blur-[2px]" onClick={() => setActive(null)}>
          <aside onClick={(e) => e.stopPropagation()} className="h-full w-full max-w-md overflow-y-auto border-l border-[#e6eae2] bg-[#f7f8f4] p-6 dark:border-white/10 dark:bg-[#10241e]">
            <div className="flex items-start justify-between">
              <div>
                <p className="font-mono text-[12px] text-[#8a968e]">{active.id}</p>
                <h3 className="mt-1 text-[18px] font-semibold">{active.type}</h3>
              </div>
              <button onClick={() => setActive(null)} className="rounded-full p-1.5 hover:bg-white dark:hover:bg-white/8">
                <X className="h-4 w-4" />
              </button>
            </div>
            <p className="mt-2 text-[13px] text-[#6b7a72]">{active.party} · {active.filename ?? active.size}</p>
            <div className="mt-5 space-y-3">
              {(active.fields?.length
                ? active.fields
                : [
                    { label: "Type", value: active.type, confidence: 0.92 },
                    { label: "Shipment", value: active.shipmentId, confidence: 0.9 },
                    { label: "Party", value: active.party, confidence: 0.84 },
                    { label: "Updated", value: active.updated, confidence: 0.99 },
                  ]
              ).map((f) => (
                <div key={f.label} className="rounded-xl bg-white p-3 ring-1 ring-[#eef1ea] dark:bg-white/5 dark:ring-white/8">
                  <div className="flex items-center justify-between text-[11px] text-[#8a968e]">
                    <span>{f.label}</span>
                    <span>{Math.round(f.confidence * 100)}%</span>
                  </div>
                  <p className="mt-1 text-[14px] font-semibold">{f.value}</p>
                  <div className="mt-2 h-1 overflow-hidden rounded-full bg-[#eef1ea] dark:bg-white/10">
                    <div className="h-full bg-[#A3E635]" style={{ width: `${f.confidence * 100}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </aside>
        </div>
      )}
    </div>
  );
}
