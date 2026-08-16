"use client"

import { notFound } from "next/navigation"
import { useShipment } from "@/lib/hooks"
import { ShipmentDetail } from "@/components/shipment-detail"
import { Loader2 } from "lucide-react"

interface ShipmentDetailPageProps {
  params: Promise<{ id: string }>
}

export default function ShipmentDetailPage({ params }: ShipmentDetailPageProps) {
  const { id } = await params
  const { data: shipment, isLoading, error } = useShipment(id)

  if (isLoading) {
    return (
      <div className="mx-auto flex max-w-[1400px] flex-col gap-6">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Loader2 className="size-4 animate-spin" />
          <span>Loading shipment...</span>
        </div>
        <div className="rounded-2xl border border-border bg-card p-6 animate-pulse">
          <div className="h-8 bg-muted rounded w-1/4 mb-4" />
          <div className="h-4 bg-muted rounded w-1/2" />
        </div>
      </div>
    )
  }

  if (error || !shipment) {
    notFound()
  }

  return <ShipmentDetail shipment={shipment} />
}