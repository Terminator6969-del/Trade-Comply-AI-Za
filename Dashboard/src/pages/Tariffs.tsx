import { useMemo, useState } from "react";
import { hsCodes } from "../lib/data";
import { parseDutyRate } from "../lib/ops";
import { Card } from "../components/ui";
import { Calculator, Search } from "lucide-react";
import { formatZar } from "../lib/format";

export function Tariffs() {
  const [q, setQ] = useState("");
  const [code, setCode] = useState(hsCodes[0].code);
  const [cif, setCif] = useState("4285000");
  const [kg, setKg] = useState("18400");
  const rows = useMemo(() => {
    const n = q.toLowerCase();
    return hsCodes.filter((h) => h.code.includes(n) || h.description.toLowerCase().includes(n) || h.notes.toLowerCase().includes(n));
  }, [q]);
  const selected = hsCodes.find((h) => h.code === code) ?? hsCodes[0];
  const rate = parseDutyRate(selected.duty);
  const cifN = Number(cif) || 0;
  const kgN = Number(kg) || 0;
  const duty = cifN * rate.pct + kgN * rate.perKg;
  const vat = selected.vat.includes("0%") ? 0 : (cifN + duty) * 0.15;

  return (
    <div className="space-y-5">
      <div>
        <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-[#8a968e]">Classification</p>
        <h1 className="mt-1 text-[28px] font-semibold tracking-tight">Tariffs & HS codes</h1>
        <p className="mt-1 text-[13.5px] text-[#6b7a72]">
          Working set mapped to the SARS Schedule and ITAC permit matrix.
        </p>
      </div>
      <div className="grid grid-cols-1 gap-3 xl:grid-cols-12">
        <Card className="xl:col-span-7">
          <div className="flex items-center gap-2">
            <Calculator className="h-4 w-4 text-[#0F2B24] dark:text-[#B7EE55]" />
            <h3 className="text-[15px] font-semibold">Duty calculator</h3>
          </div>
          <p className="mt-1 text-[12px] text-[#6b7a72]">SARS Schedule 1 estimate · VAT 15% unless export zero-rated.</p>
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
            <label className="text-[12px] font-medium text-[#6b7a72]">
              HS code
              <select value={code} onChange={(e) => setCode(e.target.value)} className="mt-1 h-10 w-full rounded-xl border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5">
                {hsCodes.map((h) => <option key={h.code} value={h.code}>{h.code}</option>)}
              </select>
            </label>
            <label className="text-[12px] font-medium text-[#6b7a72]">
              CIF value (ZAR)
              <input value={cif} onChange={(e) => setCif(e.target.value)} type="number" className="mt-1 h-10 w-full rounded-xl border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5" />
            </label>
            <label className="text-[12px] font-medium text-[#6b7a72]">
              Net mass (kg)
              <input value={kg} onChange={(e) => setKg(e.target.value)} type="number" className="mt-1 h-10 w-full rounded-xl border border-[#e2e7de] bg-white px-3 text-[13px] dark:border-white/10 dark:bg-white/5" />
            </label>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-3">
            <div className="rounded-xl bg-[#f4f6f0] p-3 dark:bg-white/5">
              <p className="text-[11px] text-[#8a968e]">Duty</p>
              <p className="mt-1 tabular text-[18px] font-semibold">{formatZar(duty)}</p>
            </div>
            <div className="rounded-xl bg-[#f4f6f0] p-3 dark:bg-white/5">
              <p className="text-[11px] text-[#8a968e]">VAT</p>
              <p className="mt-1 tabular text-[18px] font-semibold">{formatZar(vat)}</p>
            </div>
            <div className="rounded-xl bg-[#0F2B24] p-3 text-white">
              <p className="text-[11px] text-white/60">Payable</p>
              <p className="mt-1 tabular text-[18px] font-semibold text-[#B7EE55]">{formatZar(duty + vat)}</p>
            </div>
          </div>
          <p className="mt-3 text-[12px] text-[#6b7a72]">{selected.description} · {selected.duty} · {selected.permit}</p>
        </Card>
        <Card className="xl:col-span-5">
          <h3 className="text-[15px] font-semibold">Search the working set</h3>
          <div className="relative mt-3">
            <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-[#8a968e]" />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search HS code or description…"
              className="h-11 w-full rounded-full border border-[#e2e7de] bg-white pl-10 pr-4 text-[13px] dark:border-white/10 dark:bg-white/5"
            />
          </div>
          <p className="mt-3 text-[12px] text-[#6b7a72]">{rows.length} headings match · mapped to SARS Schedule 1.</p>
        </Card>
      </div>
      <div className="grid grid-cols-1 gap-3">
        {rows.map((h) => (
          <Card key={h.code}>
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="font-mono text-[15px] font-semibold text-[#0F2B24] dark:text-[#B7EE55]">{h.code}</p>
                <p className="mt-1 text-[14px] font-medium">{h.description}</p>
                <p className="mt-2 text-[13px] text-[#6b7a72]">{h.notes}</p>
              </div>
              <div className="flex flex-wrap gap-2 sm:justify-end">
                <span className="rounded-full bg-[#0F2B24] px-2.5 py-1 text-[11px] font-semibold text-[#B7EE55]">
                  Duty {h.duty}
                </span>
                <span className="rounded-full bg-[#eef1ea] px-2.5 py-1 text-[11px] font-semibold text-[#0F2B24] dark:bg-white/8 dark:text-white">
                  VAT {h.vat}
                </span>
                {h.itac && (
                  <span className="rounded-full bg-amber-50 px-2.5 py-1 text-[11px] font-semibold text-amber-700">
                    ITAC
                  </span>
                )}
                <span className="rounded-full bg-white px-2.5 py-1 text-[11px] font-semibold ring-1 ring-[#e2e7de] dark:bg-transparent dark:ring-white/10">
                  {h.permit}
                </span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
