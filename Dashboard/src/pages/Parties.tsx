import { useState } from "react";
import { Plus, X } from "lucide-react";
import { Card, RiskBadge } from "../components/ui";
import { formatDate } from "../lib/format";
import { useApp } from "../lib/store";
import { useCreateParty } from "../lib/api";
import type { Risk, TradeParty } from "../lib/types";

export function Parties() {
  const parties = useApp((s) => s.parties);
  const create = useCreateParty();
  const [open, setOpen] = useState(false);
  const [role, setRole] = useState("all");
  const [form, setForm] = useState({ name: "", role: "Importer" as TradeParty["role"], city: "Cape Town", tin: "", contact: "" });
  const list = role === "all" ? parties : parties.filter((p) => p.role === role);

  const submit = () => {
    if (!form.name) return;
    const p: TradeParty = {
      id: `P-${String(parties.length + 1).padStart(2, "0")}`,
      name: form.name,
      role: form.role,
      country: "South Africa",
      city: form.city,
      tin: form.tin || "VAT pending",
      risk: "low" as Risk,
      shipments: 0,
      lastActive: new Date().toISOString().slice(0, 10),
      contact: form.contact || "ops@tradecomply.ai",
    };
    create.mutate(p);
    setOpen(false);
    setForm({ name: "", role: "Importer", city: "Cape Town", tin: "", contact: "" });
  };

  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-[#8a968e]">Network</p>
          <h1 className="mt-1 text-[28px] font-semibold tracking-tight">Trade parties</h1>
          <p className="mt-1 text-[13.5px] text-[#6b7a72]">Importers, exporters, carriers and licensed clearing agents.</p>
        </div>
        <button onClick={() => setOpen(true)} className="inline-flex h-10 items-center gap-2 rounded-full bg-[#0F2B24] px-4 text-[13px] font-semibold text-white dark:bg-[#A3E635] dark:text-[#0F2B24]">
          <Plus className="h-4 w-4" /> New party
        </button>
      </div>
      <div className="flex flex-wrap gap-2">
        {["all", "Importer", "Exporter", "Carrier", "Broker", "Consignee"].map((r) => (
          <button key={r} onClick={() => setRole(r)} className={`rounded-full px-3 py-1.5 text-[12px] font-semibold ${role === r ? "bg-[#0F2B24] text-white dark:bg-[#A3E635] dark:text-[#0F2B24]" : "bg-white ring-1 ring-[#e2e7de] dark:bg-white/5 dark:ring-white/10"}`}>
            {r === "all" ? "All roles" : r}
          </button>
        ))}
      </div>
      <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
        {list.map((p) => (
          <Card key={p.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-[15px] font-semibold">{p.name}</p>
                <p className="text-[12px] text-[#6b7a72]">
                  {p.role} · {p.city}, {p.country}
                </p>
              </div>
              <RiskBadge risk={p.risk} />
            </div>
            <dl className="mt-4 grid grid-cols-2 gap-3 text-[12.5px]">
              <div>
                <dt className="text-[#8a968e]">Tax / ID</dt>
                <dd className="mt-0.5 font-medium">{p.tin}</dd>
              </div>
              <div>
                <dt className="text-[#8a968e]">Shipments</dt>
                <dd className="mt-0.5 font-medium tabular">{p.shipments}</dd>
              </div>
              <div>
                <dt className="text-[#8a968e]">Last active</dt>
                <dd className="mt-0.5 font-medium">{formatDate(p.lastActive)}</dd>
              </div>
              <div>
                <dt className="text-[#8a968e]">Contact</dt>
                <dd className="mt-0.5 truncate font-medium">{p.contact}</dd>
              </div>
            </dl>
          </Card>
        ))}
      </div>

      {open && (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-[#0F2B24]/30 p-3 backdrop-blur-sm sm:items-center" onClick={() => setOpen(false)}>
          <div onClick={(e) => e.stopPropagation()} className="w-full max-w-md rounded-3xl bg-[#f7f8f4] p-6 dark:bg-[#10241e]">
            <div className="flex items-center justify-between">
              <h3 className="text-[18px] font-semibold">Add party</h3>
              <button onClick={() => setOpen(false)} className="rounded-full p-1.5 hover:bg-white dark:hover:bg-white/8"><X className="h-4 w-4" /></button>
            </div>
            <div className="mt-4 space-y-3">
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Legal name" className="h-10 w-full rounded-xl border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5" />
              <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value as TradeParty["role"] })} className="h-10 w-full rounded-xl border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5">
                {["Importer", "Exporter", "Carrier", "Broker", "Consignee"].map((r) => <option key={r}>{r}</option>)}
              </select>
              <input value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} placeholder="City" className="h-10 w-full rounded-xl border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5" />
              <input value={form.tin} onChange={(e) => setForm({ ...form, tin: e.target.value })} placeholder="VAT / TIN" className="h-10 w-full rounded-xl border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5" />
              <input value={form.contact} onChange={(e) => setForm({ ...form, contact: e.target.value })} placeholder="Email" className="h-10 w-full rounded-xl border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5" />
            </div>
            <button onClick={submit} className="mt-5 h-10 w-full rounded-full bg-[#0F2B24] text-[13px] font-semibold text-white dark:bg-[#A3E635] dark:text-[#0F2B24]">Save party</button>
          </div>
        </div>
      )}
    </div>
  );
}
