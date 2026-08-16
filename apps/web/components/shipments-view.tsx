"use client"

import { useMemo, useState } from "react"
import Link from "next/link"
import { Search, Plus, Plane, Ship as ShipIcon, Truck } from "lucide-react"
import type { Shipment, ShipmentStatus, ShipmentDirection } from "@/lib/types"
import { ShipmentStatusBadge, ComplianceBadge } from "@/components/status-badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog"
import { formatCurrency, formatDate, cn } from "@/lib/utils"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const modeIcon = { sea: ShipIcon, air: Plane, road: Truck }

const statusFilters: { value: ShipmentStatus | "all"; label: string }[] = [
  { value: "all", label: "All" },
  { value: "in_transit", label: "In transit" },
  { value: "at_customs", label: "At customs" },
  { value: "held", label: "Held" },
  { value: "cleared", label: "Cleared" },
  { value: "draft", label: "Draft" },
]

export function ShipmentsView({ initialShipments }: { initialShipments: Shipment[] }) {
  const [query, setQuery] = useState("")
  const [status, setStatus] = useState<ShipmentStatus | "all">("all")
  const [direction, setDirection] = useState<ShipmentDirection | "all">("all")
  const [open, setOpen] = useState(false)

  const filtered = useMemo(() => {
    return initialShipments.filter((s) => {
      const matchesQuery =
        !query ||
        s.reference.toLowerCase().includes(query.toLowerCase()) ||
        s.importer.toLowerCase().includes(query.toLowerCase()) ||
        s.supplier.toLowerCase().includes(query.toLowerCase())
      const matchesStatus = status === "all" || s.status === status
      const matchesDir = direction === "all" || s.direction === direction
      return matchesQuery && matchesStatus && matchesDir
    })
  }, [initialShipments, query, status, direction])

  return (
    <div className="flex flex-col gap-5">
      {/* Filters */}
      <div className="flex flex-col gap-3 rounded-2xl border border-border bg-card p-4 lg:flex-row lg:items-center">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by reference, importer or supplier"
            className="h-10 w-full rounded-xl border border-border bg-background pl-9 pr-3 text-sm outline-none focus:border-primary/40 focus:ring-2 focus:ring-primary/15"
          />
        </div>
        <div className="flex flex-wrap items-center gap-1.5">
          {statusFilters.map((f) => (
            <button
              key={f.value}
              onClick={() => setStatus(f.value)}
              className={cn(
                "rounded-lg px-3 py-1.5 text-xs font-medium transition-colors",
                status === f.value
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted text-muted-foreground hover:bg-muted/70",
              )}
            >
              {f.label}
            </button>
          ))}
        </div>
        <Select value={direction} onValueChange={(v) => setDirection(v as ShipmentDirection | "all")}>
          <SelectTrigger className="h-10 w-[180px]">
            <SelectValue placeholder="All directions" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All directions</SelectItem>
            <SelectItem value="import">Imports</SelectItem>
            <SelectItem value="export">Exports</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          {filtered.length} of {initialShipments.length} shipments
        </p>
        <Button className="gap-1.5" onClick={() => setOpen(true)}>
          <Plus className="size-4" /> New shipment
        </Button>
      </div>

      {/* Table */}
      <div className="overflow-hidden rounded-2xl border border-border bg-card">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[820px] text-sm">
            <thead>
              <tr className="border-b border-border text-left text-xs uppercase tracking-wide text-muted-foreground">
                <th className="px-5 py-3 font-medium">Reference</th>
                <th className="px-5 py-3 font-medium">Lane</th>
                <th className="px-5 py-3 font-medium">Importer</th>
                <th className="px-5 py-3 font-medium">Value</th>
                <th className="px-5 py-3 font-medium">Compliance</th>
                <th className="px-5 py-3 font-medium">Status</th>
                <th className="px-5 py-3 font-medium">ETA</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {filtered.map((s) => {
                const Icon = modeIcon[s.mode]
                return (
                  <tr key={s.id} className="group transition-colors hover:bg-muted/50">
                    <td className="px-5 py-3.5">
                      <Link href={`/shipments/${s.id}`} className="flex items-center gap-2.5">
                        <span className="flex size-8 items-center justify-center rounded-lg bg-muted text-muted-foreground">
                          <Icon className="size-4" />
                        </span>
                        <span>
                          <span className="block font-semibold text-foreground group-hover:text-primary">
                            {s.reference}
                          </span>
                          <span className="block text-xs uppercase text-muted-foreground">
                            {s.direction}
                          </span>
                        </span>
                      </Link>
                    </td>
                    <td className="px-5 py-3.5 text-muted-foreground">
                      {s.origin} → {s.destination}
                    </td>
                    <td className="px-5 py-3.5 text-foreground">{s.importer}</td>
                    <td className="px-5 py-3.5 font-medium text-foreground">
                      {formatCurrency(s.value, s.currency)}
                    </td>
                    <td className="px-5 py-3.5">
                      <ComplianceBadge status={s.compliance} />
                    </td>
                    <td className="px-5 py-3.5">
                      <ShipmentStatusBadge status={s.status} />
                    </td>
                    <td className="px-5 py-3.5 text-muted-foreground">{formatDate(s.eta)}</td>
                  </tr>
                )
              })}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-5 py-12 text-center text-muted-foreground">
                    No shipments match your filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <CreateShipmentModal open={open} onOpenChange={setOpen} />
    </div>
  )
}

function CreateShipmentModal({
  open,
  onOpenChange,
}: {
  open: boolean
  onOpenChange: (v: boolean) => void
}) {
  const inputClass =
    "h-10 w-full rounded-xl border border-border bg-background px-3 text-sm outline-none focus:border-primary/40 focus:ring-2 focus:ring-primary/15"
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>Create shipment</DialogTitle>
          <DialogDescription>
            Register a new consignment. AI extraction runs once documents are attached.
          </DialogDescription>
        </DialogHeader>
        <form
          className="grid gap-4 py-1 sm:grid-cols-2"
          onSubmit={(e) => {
            e.preventDefault()
            onOpenChange(false)
          }}
        >
          <div className="sm:col-span-2">
            <label className="mb-1.5 block text-xs font-medium text-foreground">Reference</label>
            <input className={inputClass} placeholder="TCA-2025-XXXX" />
          </div>
          <div>
            <label className="mb-1.5 block text-xs font-medium text-foreground">Direction</label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Select direction" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="import">Import</SelectItem>
                <SelectItem value="export">Export</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="mb-1.5 block text-xs font-medium text-foreground">Transport mode</label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Select mode" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="sea">Sea</SelectItem>
                <SelectItem value="air">Air</SelectItem>
                <SelectItem value="road">Road</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="mb-1.5 block text-xs font-medium text-foreground">Origin</label>
            <input className={inputClass} placeholder="Shanghai, CN" />
          </div>
          <div>
            <label className="mb-1.5 block text-xs font-medium text-foreground">Destination</label>
            <input className={inputClass} placeholder="Durban, ZA" />
          </div>
          <div className="sm:col-span-2">
            <label className="mb-1.5 block text-xs font-medium text-foreground">Importer / consignee</label>
            <input className={inputClass} placeholder="Company name" />
          </div>
        </form>
        <DialogFooter>
          <DialogClose render={<Button variant="outline" />}>Cancel</DialogClose>
          <Button onClick={() => onOpenChange(false)}>Create shipment</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}