import { Plus } from "lucide-react";
import { ShipmentsTable } from "../components/ShipmentsTable";
import { FilterBar } from "../components/FilterBar";
import { useApp } from "../lib/store";
import { useShipmentsQuery } from "../lib/api";
import { TableSkeleton } from "../components/Skeleton";

export function Shipments() {
  const setModalOpen = useApp((s) => s.setModalOpen);
  const { isFetching, isLoading } = useShipmentsQuery();
  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-[#8a968e]">Operations</p>
          <h1 className="mt-1 text-[28px] font-semibold tracking-tight text-[#12211c] dark:text-white">Shipments</h1>
          <p className="mt-1 text-[13.5px] text-[#6b7a72]">
            Live book across Cape Town, Durban and Johannesburg inland terminals.
          </p>
        </div>
        <button
          onClick={() => setModalOpen(true)}
          className="inline-flex h-10 items-center gap-2 rounded-full bg-[#0F2B24] px-4 text-[13px] font-semibold text-white dark:bg-[#A3E635] dark:text-[#0F2B24]"
        >
          <Plus className="h-4 w-4" />
          New shipment
        </button>
      </div>
      <FilterBar />
      {isLoading && !isFetching ? <TableSkeleton /> : <ShipmentsTable />}
    </div>
  );
}
