"use client"

import { ShieldCheck, AlertTriangle, TrendingUp, type LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"

interface Insight {
  type: "success" | "warning" | "info"
  title: string
  description: string
  icon: LucideIcon
}

const insights: Insight[] = [
  {
    type: "success",
    title: "HS Code Recommendation",
    description: "Solar panel shipments may qualify for reduced duty under heading 8541.40",
    icon: ShieldCheck,
  },
  {
    type: "warning",
    title: "Document Alert",
    description: "3 shipments missing NRCS certificates for textile imports",
    icon: AlertTriangle,
  },
  {
    type: "info",
    title: "Cost Savings",
    description: "Correct HS classification saved R45,000 in duties this month",
    icon: TrendingUp,
  },
]

const typeStyles = {
  success: "bg-green-100 text-green-700",
  warning: "bg-amber-100 text-amber-700",
  info: "bg-blue-100 text-blue-700",
}

export function AIInsightsWidget() {
  return (
    <div className="rounded-2xl border border-border bg-card p-6">
      <h2 className="text-base font-semibold text-foreground">AI Insights</h2>
      <div className="mt-4 space-y-3">
        {insights.map((insight, i) => (
          <div key={i} className="flex items-start gap-3 p-4 rounded-xl bg-muted/50">
            <div className={cn("flex size-8 items-center justify-center rounded-lg", typeStyles[insight.type])}>
              <insight.icon className="size-4" />
            </div>
            <div>
              <p className="text-sm font-medium text-foreground">{insight.title}</p>
              <p className="mt-1 text-xs text-muted-foreground">{insight.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}