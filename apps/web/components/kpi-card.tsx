"use client"

import { ArrowUpRight, ArrowDownRight, type LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"

export function KpiCard({
  label,
  value,
  delta,
  trend = "up",
  icon: Icon,
  highlight = false,
}: {
  label: string
  value: string
  delta?: string
  trend?: "up" | "down"
  icon: LucideIcon
  highlight?: boolean
}) {
  return (
    <div
      className={cn(
        "rounded-2xl border p-5 transition-shadow hover:shadow-sm",
        highlight
          ? "border-transparent bg-primary text-primary-foreground"
          : "border-border bg-card",
      )}
    >
      <div className="flex items-center justify-between">
        <div
          className={cn(
            "flex size-9 items-center justify-center rounded-xl",
            highlight ? "bg-primary-foreground/15" : "bg-primary/10 text-primary",
          )}
        >
          <Icon className="size-[18px]" />
        </div>
        {delta ? (
          <span
            className={cn(
              "flex items-center gap-0.5 text-xs font-semibold",
              highlight
                ? "text-primary-foreground/90"
                : trend === "up"
                  ? "text-primary"
                  : "text-red-600",
            )}
          >
            {trend === "up" ? (
              <ArrowUpRight className="size-3.5" />
            ) : (
              <ArrowDownRight className="size-3.5" />
            )}
            {delta}
          </span>
        ) : null}
      </div>
      <p
        className={cn(
          "mt-4 text-3xl font-bold tracking-tight",
          highlight ? "text-primary-foreground" : "text-foreground",
        )}
      >
        {value}
      </p>
      <p
        className={cn(
          "mt-1 text-sm",
          highlight ? "text-primary-foreground/80" : "text-muted-foreground",
        )}
      >
        {label}
      </p>
    </div>
  )
}