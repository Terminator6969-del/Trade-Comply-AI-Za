import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";
import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useApp } from "../lib/store";
import type { Lane, Shipment } from "../lib/types";

export function NewShipmentModal() {
  const { modalOpen, setModalOpen, addShipment, parties } = useApp();
  const nav = useNavigate();
  const [partyOpen, setPartyOpen] = useState(false);
  const [form, setForm] = useState({
    company: "",
    origin: "Rotterdam",
    destination: "Cape Town",
    lane: "EU" as Lane,
    flow: "import" as "import" | "export",
    value: "1250000",
    hsCode: "6109.10",
    mode: "Ocean" as Shipment["mode"],
  });
  const partyHits = parties.filter((p) =>
    p.name.toLowerCase().includes(form.company.toLowerCase()),
  ).slice(0, 6);

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    const n = Math.floor(1000 + Math.random() * 8999);
    const id = `TC-2604-${n}`;
    const ship: Shipment = {
      id,
      company: form.company || "New consignee",
      origin: form.origin,
      destination: form.destination,
      lane: form.lane,
      flow: form.flow,
      status: "draft",
      risk: "low",
      value: Number(form.value) || 0,
      duty: Math.round((Number(form.value) || 0) * 0.08),
      date: new Date().toISOString().slice(0, 10),
      eta: new Date(Date.now() + 12 * 86400000).toISOString().slice(0, 10),
      hsCode: form.hsCode,
      hsDesc: "Pending AI classification",
      mode: form.mode,
      consignee: form.company || "New consignee",
      broker: "Bidvest Panalpina",
      sarsRef: "—",
      weight: 0,
      containers: 1,
      docs: 0,
      notes: "Created from dashboard. Awaiting commercial invoice.",
    };
    addShipment(ship);
    setModalOpen(false);
    nav(`/shipments/${id}`);
  };

  const field =
    "h-10 w-full rounded-xl border border-[#e2e7de] bg-white px-3 text-[13px] outline-none ring-[#A3E635]/50 focus:ring-2 dark:border-white/10 dark:bg-white/5 dark:text-white";

  return (
    <AnimatePresence>
      {modalOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-end justify-center bg-[#0F2B24]/35 p-3 backdrop-blur-sm sm:items-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setModalOpen(false)}
        >
          <motion.form
            onSubmit={onSubmit}
            onClick={(e) => e.stopPropagation()}
            initial={{ y: 40, opacity: 0, scale: 0.96 }}
            animate={{ y: 0, opacity: 1, scale: 1 }}
            exit={{ y: 24, opacity: 0, scale: 0.96 }}
            transition={{ type: "spring", stiffness: 380, damping: 28 }}
            className="w-full max-w-[520px] rounded-3xl border border-[#e6eae2] bg-[#f7f8f4] p-6 shadow-2xl dark:border-white/10 dark:bg-[#10241e]"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[#8a968e]">New entry</p>
                <h2 className="mt-1 text-xl font-semibold text-[#12211c] dark:text-white">Create shipment</h2>
              </div>
              <button
                type="button"
                onClick={() => setModalOpen(false)}
                className="rounded-full p-1.5 hover:bg-white dark:hover:bg-white/8"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="mt-5 grid grid-cols-2 gap-3">
              <label className="relative col-span-2 text-[12px] font-medium text-[#5c6b64]">
                Company / party
                <input
                  required
                  value={form.company}
                  onChange={(e) => { setForm({ ...form, company: e.target.value }); setPartyOpen(true); }}
                  onFocus={() => setPartyOpen(true)}
                  className={`mt-1 ${field}`}
                  placeholder="Type to search parties…"
                  autoComplete="off"
                />
                {partyOpen && partyHits.length > 0 && (
                  <div className="absolute left-0 right-0 top-full z-10 mt-1 overflow-hidden rounded-xl border border-[#e2e7de] bg-white py-1 shadow-lg dark:border-white/10 dark:bg-[#132821]">
                    {partyHits.map((p) => (
                      <button
                        type="button"
                        key={p.id}
                        onClick={() => { setForm({ ...form, company: p.name }); setPartyOpen(false); }}
                        className="block w-full px-3 py-2 text-left text-[13px] hover:bg-[#f4f6f0] dark:hover:bg-white/5"
                      >
                        <span className="font-semibold">{p.name}</span>
                        <span className="ml-2 text-[11px] text-[#8a968e]">{p.role} · {p.city}</span>
                      </button>
                    ))}
                  </div>
                )}
              </label>
              <label className="text-[12px] font-medium text-[#5c6b64]">
                Origin
                <input value={form.origin} onChange={(e) => setForm({ ...form, origin: e.target.value })} className={`mt-1 ${field}`} />
              </label>
              <label className="text-[12px] font-medium text-[#5c6b64]">
                Destination
                <input
                  value={form.destination}
                  onChange={(e) => setForm({ ...form, destination: e.target.value })}
                  className={`mt-1 ${field}`}
                />
              </label>
              <label className="text-[12px] font-medium text-[#5c6b64]">
                Trade lane
                <select
                  value={form.lane}
                  onChange={(e) => setForm({ ...form, lane: e.target.value as Lane })}
                  className={`mt-1 ${field}`}
                >
                  {["EU", "Asia", "SADC", "UK", "Americas"].map((l) => (
                    <option key={l}>{l}</option>
                  ))}
                </select>
              </label>
              <label className="text-[12px] font-medium text-[#5c6b64]">
                Flow
                <select
                  value={form.flow}
                  onChange={(e) => setForm({ ...form, flow: e.target.value as "import" | "export" })}
                  className={`mt-1 ${field}`}
                >
                  <option value="import">Import</option>
                  <option value="export">Export</option>
                </select>
              </label>
              <label className="text-[12px] font-medium text-[#5c6b64]">
                Customs value (ZAR)
                <input
                  type="number"
                  value={form.value}
                  onChange={(e) => setForm({ ...form, value: e.target.value })}
                  className={`mt-1 ${field}`}
                />
              </label>
              <label className="text-[12px] font-medium text-[#5c6b64]">
                HS code
                <input value={form.hsCode} onChange={(e) => setForm({ ...form, hsCode: e.target.value })} className={`mt-1 ${field}`} />
              </label>
              <label className="col-span-2 text-[12px] font-medium text-[#5c6b64]">
                Mode
                <select
                  value={form.mode}
                  onChange={(e) => setForm({ ...form, mode: e.target.value as Shipment["mode"] })}
                  className={`mt-1 ${field}`}
                >
                  <option>Ocean</option>
                  <option>Air</option>
                  <option>Road</option>
                  <option>Rail</option>
                </select>
              </label>
            </div>

            <div className="mt-6 flex items-center justify-end gap-2">
              <button
                type="button"
                onClick={() => setModalOpen(false)}
                className="h-10 rounded-full px-4 text-[13px] font-semibold text-[#5c6b64] hover:bg-white dark:hover:bg-white/8"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="h-10 rounded-full bg-[#0F2B24] px-5 text-[13px] font-semibold text-white hover:bg-[#16382f] dark:bg-[#A3E635] dark:text-[#0F2B24]"
              >
                Create draft
              </button>
            </div>
          </motion.form>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
