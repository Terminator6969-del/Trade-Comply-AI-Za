"use client"

import Link from "next/link"
import { notFound } from "next/navigation"
import {
  ArrowLeft,
  Plane,
  Ship as ShipIcon,
  Truck,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  FileText,
  Building2,
  MapPin,
  CalendarDays,
} from "lucide-react"
import { ShipmentStatusBadge, ComplianceBadge } from "@/components/status-badge"
import { MiniBar } from "@/components/charts"
import { Button } from "@/components/ui/button"
import { formatCurrency, formatDate } from "@/lib/utils"
import type { ComplianceCheck, ShipmentDocument } from "@/lib/types"

const modeIcon = { sea: ShipIcon, air: Plane, road: Truck }
const modeLabel = { sea: "Sea freight", air: "Air freight", road: "Road freight" }

const checkIcon = {
  pass: { icon: CheckCircle2, cls: "text-primary" },
  warning: { icon: AlertTriangle, cls: "text-amber-600" },
  fail: { icon: XCircle, cls: "text-red-600" },
}

const docStatusStyles: Record<ShipmentDocument["status"], string> = {
  extracted: "bg-primary/10 text-primary",
  processing: "bg-sky-100 text-sky-700",
  review_required: "bg-amber-100 text-amber-700",
  failed: "bg-red-100 text-red-700",
}

interface ShipmentDetailProps {
  shipment: {
    id: string
    reference: string
    direction: "import" | "export"
    status: string
    compliance: string
    importer: string
    supplier: string
    origin: string
    destination: string
    mode: "sea" | "air" | "road"
    value: number
    currency: string
    eta: string
    createdAt: string
    riskScore: number
    lineItems: Array<{
      id: string
      description: string
      hsCode: string
      quantity: number
      unitValue: number
      origin: string
      dutyRate: number
    }>
    documents: ShipmentDocument[]
    checks: ComplianceCheck[]
  }
}

export function ShipmentDetail({ shipment }: ShipmentDetailProps) {
  const Icon = modeIcon[shipment.mode]
  const totalValue = shipment.lineItems.reduce((s, li) => s + li.quantity * li.unitValue, 0)

  return (
    <div className="mx-auto flex max-w-[1400px] flex-col gap-6">
      <Link
        href="/shipments"
        className="flex w-fit items-center gap-1.5 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
      >
        <ArrowLeft className="size-4" /> Back to shipments
      </Link>

      {/* Header */}
      <div className="rounded-2xl border border-border bg-card p-6">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex size-12 items-center justify-center rounded-2xl bg-primary/10 text-primary">
              <Icon className="size-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold text-foreground">{shipment.reference}</h1>
                <span className="text-xs font-medium uppercase text-muted-foreground">
                  {shipment.direction}
                </span>
              </div>
              <p className="text-sm text-muted-foreground">
                {modeLabel[shipment.mode]} · {shipment.origin} → {shipment.destination}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <ComplianceBadge status={shipment.compliance as any} />
            <ShipmentStatusBadge status={shipment.status as any} />
            <Button className="ml-2">Submit to SARS</Button>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-2 gap-4 border-t border-border pt-5 md:grid-cols-4">
          <Meta icon={Building2} label="Importer" value={shipment.importer} />
          <Meta icon={Building2} label="Supplier" value={shipment.supplier} />
          <Meta icon={MapPin} label="Route" value={`${shipment.origin} → ${shipment.destination}`} />
          <Meta icon={CalendarDays} label="ETA" value={formatDate(shipment.eta)} />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="flex flex-col gap-6 lg:col-span-2">
          {/* Line items */}
          <section className="rounded-2xl border border-border bg-card">
            <div className="border-b border-border px-5 py-4">
              <h2 className="text-base font-semibold text-foreground">Line items</h2>
              <p className="text-xs text-muted-foreground">Declared goods and tariff classification</p>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full min-w-[560px] text-sm">
                <thead>
                  <tr className="border-b border-border text-left text-xs uppercase tracking-wide text-muted-foreground">
                    <th className="px-5 py-3 font-medium">Description</th>
                    <th className="px-5 py-3 font-medium">HS code</th>
                    <th className="px-5 py-3 font-medium">Qty</th>
                    <th className="px-5 py-3 font-medium">Duty</th>
                    <th className="px-5 py-3 text-right font-medium">Line value</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {shipment.lineItems.map((li) => (
                    <tr key={li.id}>
                      <td className="px-5 py-3.5 font-medium text-foreground">{li.description}</td>
                      <td className="px-5 py-3.5 font-mono text-xs text-muted-foreground">{li.hsCode}</td>
                      <td className="px-5 py-3.5 text-muted-foreground">{li.quantity.toLocaleString()}</td>
                      <td className="px-5 py-3.5 text-muted-foreground">{li.dutyRate}%</td>
                      <td className="px-5 py-3.5 text-right font-medium text-foreground">
                        {formatCurrency(li.quantity * li.unitValue, shipment.currency)}
                      </td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr className="border-t border-border">
                    <td colSpan={4} className="px-5 py-3.5 text-right text-sm font-medium text-muted-foreground">
                      Declared total
                    </td>
                    <td className="px-5 py-3.5 text-right text-base font-bold text-foreground">
                      {formatCurrency(totalValue, shipment.currency)}
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </section>

          {/* Documents */}
          <section className="rounded-2xl border border-border bg-card">
            <div className="border-b border-border px-5 py-4">
              <h2 className="text-base font-semibold text-foreground">Documents</h2>
              <p className="text-xs text-muted-foreground">AI-extracted trade documents</p>
            </div>
            <ul className="divide-y divide-border">
              {shipment.documents.map((d) => (
                <li key={d.id} className="flex items-center gap-3 px-5 py-3.5">
                  <span className="flex size-9 items-center justify-center rounded-lg bg-muted text-muted-foreground">
                    <FileText className="size-4" />
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium text-foreground">{d.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {d.size} · {formatDate(d.uploadedAt)}
                    </p>
                  </div>
                  {d.status !== "processing" && d.status !== "failed" ? (
                    <span className="hidden text-xs text-muted-foreground sm:block">
                      {Math.round(d.confidence * 100)}% confidence
                    </span>
                  ) : null}
                  <span
                    className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${docStatusStyles[d.status]}`}
                  >
                    {d.status.replace("_", " ")}
                  </span>
                </li>
              ))}
            </ul>
          </section>
        </div>

        {/* Compliance panel */}
        <aside className="flex flex-col gap-6">
          <section className="rounded-2xl border border-border bg-card p-5">
            <h2 className="text-base font-semibold text-foreground">Risk score</h2>
            <div className="mt-4 flex items-end justify-between">
              <span className="text-4xl font-bold text-foreground">{shipment.riskScore}</span>
              <span className="text-sm text-muted-foreground">/ 100</span>
            </div>
            <MiniBar
              value={shipment.riskScore}
              className={
                shipment.riskScore > 70
                  ? "bg-red-500"
                  : shipment.riskScore > 40
                    ? "bg-amber-500"
                    : "bg-primary"
              }
            />
            <p className="mt-3 text-xs text-muted-foreground">
              Calculated from valuation, documentation completeness and sanctions screening.
            </p>
          </section>

          <section className="rounded-2xl border border-border bg-card">
            <div className="border-b border-border px-5 py-4">
              <h2 className="text-base font-semibold text-foreground">Compliance checks</h2>
              <p className="text-xs text-muted-foreground">{shipment.checks.length} rules evaluated</p>
            </div>
            <ul className="divide-y divide-border">
              {shipment.checks.map((c: ComplianceCheck) => {
                const { icon: CheckI, cls } = checkIcon[c.status]
                return (
                  <li key={c.id} className="flex gap-3 px-5 py-3.5">
                    <CheckI className={`mt-0.5 size-4 shrink-0 ${cls}`} />
                    <div>
                      <p className="text-sm font-medium text-foreground">{c.rule}</p>
                      <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">{c.detail}</p>
                    </div>
                  </li>
                )
              })}
            </ul>
          </section>
        </aside>
      </div>
    </div>
  )
}

function Meta({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Building2
  label: string
  value: string
}) {
  return (
    <div className="flex items-start gap-2.5">
      <Icon className="mt-0.5 size-4 shrink-0 text-muted-foreground" />
      <div className="min-w-0">
        <p className="text-xs text-muted-foreground">{label}</p>
        <p className="truncate text-sm font-medium text-foreground">{value}</p>
      </div>
    </div>
  )
}