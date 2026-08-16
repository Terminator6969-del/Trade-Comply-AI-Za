import { Download, Plus } from "lucide-react";
import { motion } from "framer-motion";
import { FilterBar } from "../components/FilterBar";
import { KpiCards } from "../components/KpiCards";
import { ComplianceChart, InsightsCard, LaneBars, RiskDonut } from "../components/Charts";
import { ShipmentsTable } from "../components/ShipmentsTable";
import { formatLongDate, greeting } from "../lib/format";
import { useApp } from "../lib/store";
import { shipments } from "../lib/data";

export function Overview() {
  const setModalOpen = useApp((s) => s.setModalOpen);

  const exportCsv = () => {
    const header = ["id", "company", "origin", "destination", "status", "risk", "value", "date", "hsCode"];
    const lines = [
      header.join(","),
      ...shipments.map((s) => {
        const row = s as unknown as Record<string, unknown>;
        return header.map((k) => `"${String(row[k] ?? "")}"`).join(",");
      }),
    ];
    const blob = new Blob([lines.join("\n")], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "tradecomply-shipments.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-[#8a968e]">{formatLongDate()}</p>
          <motion.h1
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-1.5 text-[32px] font-semibold leading-[1.1] tracking-tight text-[#12211c] dark:text-white sm:text-[36px]"
          >
            {greeting()}, Thandi
          </motion.h1>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={exportCsv}
            className="inline-flex h-10 items-center gap-2 rounded-full border border-[#dce2d6] bg-white px-4 text-[13px] font-semibold text-[#0F2B24] shadow-sm hover:bg-[#f4f6f0] dark:border-white/10 dark:bg-white/5 dark:text-white"
          >
            <Download className="h-4 w-4" />
            Export CSV
          </button>
          <button
            onClick={() => setModalOpen(true)}
            className="inline-flex h-10 items-center gap-2 rounded-full bg-[#0F2B24] px-4 text-[13px] font-semibold text-white shadow-sm hover:bg-[#16382f] dark:bg-[#A3E635] dark:text-[#0F2B24]"
          >
            <Plus className="h-4 w-4" />
            New shipment
          </button>
        </div>
      </div>

      <FilterBar />
      <KpiCards />

      <div className="grid grid-cols-1 gap-4 xl:grid-cols-12">
        <motion.div className="xl:col-span-8" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.12 }}>
          <ComplianceChart />
        </motion.div>
        <motion.div className="xl:col-span-4" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.16 }}>
          <RiskDonut />
        </motion.div>
        <motion.div className="xl:col-span-7" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <LaneBars />
        </motion.div>
        <motion.div className="xl:col-span-5" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.24 }}>
          <InsightsCard />
        </motion.div>
      </div>

      <ShipmentsTable compact />
    </div>
  );
}
