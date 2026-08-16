"use client"

import { Package, FileCheck, ShieldCheck, Clock, TrendingUp, Loader2 } from "lucide-react"
import { KpiCard } from "@/components/kpi-card"
import { ShipmentsView } from "@/components/shipments-view"
import { AIInsightsWidget } from "@/components/ai-insights-widget"
import { VolumeBarChart } from "@/components/charts"
import { ComplianceGauge } from "@/components/charts"
import { useShipments } from "@/lib/hooks"

export default function DashboardPage() {
  const { data: shipmentsResponse, isLoading } = useShipments()
  const shipments = shipmentsResponse?.items || []

  const activeShipments = shipments.filter((s: any) => s.status !== "cleared" && s.status !== "draft").length
  const pendingReviews = shipments.filter((s: any) => s.compliance === "at_risk" || s.compliance === "non_compliant").length
  const complianceRate = shipments.length > 0
    ? Math.round((shipments.filter((s: any) => s.compliance === "compliant").length / shipments.length) * 100)
    : 0
  const avgProcessingTime = "2.4 hrs"

  const volumeData = [
    { day: "Mon", imports: 12, exports: 8 },
    { day: "Tue", imports: 19, exports: 12 },
    { day: "Wed", imports: 15, exports: 15 },
    { day: "Thu", imports: 22, exports: 10 },
    { day: "Fri", imports: 18, exports: 14 },
    { day: "Sat", imports: 8, exports: 6 },
    { day: "Sun", imports: 4, exports: 3 },
  ]

  if (isLoading) {
    return (
      <div className="flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-foreground">Dashboard Overview</h1>
          <Loader2 className="size-4 text-primary animate-spin" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="rounded-2xl border border-border bg-card p-5 animate-pulse">
              <div className="h-4 bg-muted rounded w-3/4 mb-4" />
              <div className="h-8 bg-muted rounded w-1/2" />
              <div className="h-4 bg-muted rounded w-1/4 mt-2" />
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-foreground">Dashboard Overview</h1>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <TrendingUp className="size-4 text-primary" />
          <span>Last updated: Just now</span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <KpiCard
          label="Active Shipments"
          value={activeShipments.toString()}
          delta="+12%"
          trend="up"
          icon={Package}
        />
        <KpiCard
          label="Pending Reviews"
          value={pendingReviews.toString()}
          delta="-5%"
          trend="down"
          icon={FileCheck}
        />
        <KpiCard
          label="Compliance Rate"
          value={`${complianceRate}%`}
          delta="+2.3%"
          trend="up"
          icon={ShieldCheck}
          highlight
        />
        <KpiCard
          label="Avg Processing Time"
          value={avgProcessingTime}
          delta="-15%"
          trend="down"
          icon={Clock}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Recent Shipments + Volume Chart */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <ShipmentsView initialShipments={shipments} />

          <div className="rounded-2xl border border-border bg-card p-5">
            <h2 className="text-base font-semibold text-foreground">Weekly Volume</h2>
            <VolumeBarChart data={volumeData} />
          </div>
        </div>

        {/* Sidebar widgets */}
        <div className="flex flex-col gap-6">
          <div className="rounded-2xl border border-border bg-card p-5">
            <h2 className="text-base font-semibold text-foreground">Compliance Rate</h2>
            <ComplianceGauge value={complianceRate} />
          </div>

          <div className="rounded-2xl border border-border bg-card p-5">
            <h2 className="text-base font-semibold text-foreground">Risk Trend (6 months)</h2>
            <div className="mt-4">
              <svg viewBox="0 0 520 180" className="w-full" role="img" aria-label="Risk trend chart">
                <defs>
                  <linearGradient id="riskFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.25" />
                    <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity="0" />
                  </linearGradient>
                </defs>
                <path
                  d="M 28 152 L 126 130 L 224 110 L 322 95 L 420 85 L 518 78"
                  fill="url(#riskFill)"
                  stroke="none"
                />
                <path
                  d="M 28 152 L 126 130 L 224 110 L 322 95 L 420 85 L 518 78"
                  fill="none"
                  stroke="hsl(var(--primary))"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                />
              </svg>
            </div>
            <p className="mt-2 text-xs text-muted-foreground">Average risk score trending down</p>
          </div>

          <AIInsightsWidget />
        </div>
      </div>
    </div>
  )
}