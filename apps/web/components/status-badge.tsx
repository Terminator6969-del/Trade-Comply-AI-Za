"use client"

import { cn } from "@/lib/utils"
import type { ShipmentStatus, ComplianceStatus } from "@/lib/types"

const shipmentLabels: Record<ShipmentStatus, string> = {
  draft: "Draft",
  in_transit: "In transit",
  at_customs: "At customs",
  cleared: "Cleared",
  held: "Held",
}

const shipmentStyles: Record<ShipmentStatus, string> = {
  draft: "bg-muted text-muted-foreground",
  in_transit: "bg-sky-100 text-sky-700",
  at_customs: "bg-amber-100 text-amber-700",
  cleared: "bg-primary/10 text-primary",
  held: "bg-red-100 text-red-700",
}

const complianceLabels: Record<ComplianceStatus, string> = {
  compliant: "Compliant",
  at_risk: "At risk",
  non_compliant: "Non-compliant",
  pending: "Pending",
}

const complianceStyles: Record<ComplianceStatus, string> = {
  compliant: "bg-primary/10 text-primary",
  at_risk: "bg-amber-100 text-amber-700",
  non_compliant: "bg-red-100 text-red-700",
  pending: "bg-muted text-muted-foreground",
}

function Pill({ className, children }: { className?: string; children: React.ReactNode }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium",
        className,
      )}
    >
      <span className="size-1.5 rounded-full bg-current opacity-70" />
      {children}
    </span>
  )
}

export function ShipmentStatusBadge({ status }: { status: ShipmentStatus }) {
  return <Pill className={shipmentStyles[status]}>{shipmentLabels[status]}</Pill>
}

export function ComplianceBadge({ status }: { status: ComplianceStatus }) {
  return <Pill className={complianceStyles[status]}>{complianceLabels[status]}</Pill>
}

export function SeverityBadge({ severity }: { severity: "low" | "medium" | "high" }) {
  const styles = {
    low: "bg-muted text-muted-foreground",
    medium: "bg-amber-100 text-amber-700",
    high: "bg-red-100 text-red-700",
  }
  return <Pill className={styles[severity]}>{severity}</Pill>
}