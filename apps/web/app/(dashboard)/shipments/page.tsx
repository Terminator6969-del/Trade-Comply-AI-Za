"use client"

import { ShipmentsView } from "@/components/shipments-view"
import { useShipments } from "@/lib/hooks"

export default function ShipmentsPage() {
  const { data: shipmentsResponse, isLoading } = useShipments()
  const shipments = shipmentsResponse?.items || []

  if (isLoading) {
    return (
      <div className="flex flex-col gap-5">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-foreground">Shipments</h1>
        </div>
        <div className="rounded-2xl border border-border bg-card p-5 animate-pulse">
          <div className="h-4 bg-muted rounded w-1/4 mb-4" />
          <div className="h-64 bg-muted rounded" />
        </div>
      </div>
    )
  }

  return <ShipmentsView initialShipments={shipments} />
}