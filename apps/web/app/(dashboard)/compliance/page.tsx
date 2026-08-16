"use client"

import { ShieldCheck, AlertTriangle, XCircle, CheckCircle2, FileText, TrendingUp, Loader2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { formatDate } from "@/lib/utils"
import { useComplianceReports, useRuleViolations, useShipments, useComplianceRules } from "@/lib/hooks"

const checkIcon = {
  pass: { icon: CheckCircle2, cls: "text-primary" },
  warning: { icon: AlertTriangle, cls: "text-amber-600" },
  fail: { icon: XCircle, cls: "text-red-600" },
}

export default function CompliancePage() {
  const { data: shipmentsResponse, isLoading: shipmentsLoading } = useShipments()
  const { data: reports, isLoading: reportsLoading } = useComplianceReports()
  const { data: violations, isLoading: violationsLoading } = useRuleViolations()
  const { data: rules, isLoading: rulesLoading } = useComplianceRules()

  const isLoading = shipmentsLoading || reportsLoading || violationsLoading || rulesLoading
  const shipments = shipmentsResponse?.items || []

  const totalShipments = shipments.length
  const compliantCount = shipments.filter((s: any) => s.compliance === "compliant").length
  const atRiskCount = shipments.filter((s: any) => s.compliance === "at_risk").length
  const nonCompliantCount = shipments.filter((s: any) => s.compliance === "non_compliant").length
  const complianceRate = totalShipments > 0 ? Math.round((compliantCount / totalShipments) * 100) : 0

  if (isLoading) {
    return (
      <div className="flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-foreground">Compliance</h1>
          <Loader2 className="size-4 text-primary animate-spin" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {[1, 2, 3, 4].map((i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Loading...</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-8 bg-muted rounded w-1/2" />
                <div className="h-4 bg-muted rounded w-1/4 mt-2" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-foreground">Compliance</h1>
        <Button className="gap-2">
          <FileText className="size-4" />
          Generate Report
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Compliance Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground">{complianceRate}%</div>
            <p className="text-xs text-muted-foreground">{compliantCount} of {totalShipments} shipments</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">At Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-amber-600">{atRiskCount}</div>
            <p className="text-xs text-muted-foreground">Require attention</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Non-Compliant</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-red-600">{nonCompliantCount}</div>
            <p className="text-xs text-muted-foreground">Immediate action needed</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Violations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground">{violations?.length || 0}</div>
            <p className="text-xs text-muted-foreground">Across all shipments</p>
          </CardContent>
        </Card>
      </div>

      {/* Compliance Reports */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Compliance Reports</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border text-left text-xs uppercase tracking-wide text-muted-foreground">
                    <th className="px-5 py-3 font-medium">Period</th>
                    <th className="px-5 py-3 font-medium">Reviewed</th>
                    <th className="px-5 py-3 font-medium">Violations</th>
                    <th className="px-5 py-3 font-medium">Risk Level</th>
                    <th className="px-5 py-3 font-medium">Score</th>
                    <th className="px-5 py-3 font-medium">Generated</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {reports?.map((r: any) => (
                    <tr key={r.id} className="hover:bg-muted/50">
                      <td className="px-5 py-3.5 font-medium text-foreground">{r.period}</td>
                      <td className="px-5 py-3.5 text-muted-foreground">{r.shipmentsReviewed}</td>
                      <td className="px-5 py-3.5 text-muted-foreground">{r.violations}</td>
                      <td className="px-5 py-3.5">
                        <Badge
                          variant={
                            r.riskLevel === "low" ? "success" : r.riskLevel === "medium" ? "warning" : "destructive"
                          }
                        >
                          {r.riskLevel}
                        </Badge>
                      </td>
                      <td className="px-5 py-3.5 font-medium text-foreground">{r.score}%</td>
                      <td className="px-5 py-3.5 text-muted-foreground">{formatDate(r.generatedAt)}</td>
                    </tr>
                  ))}
                  {(!reports || reports.length === 0) && (
                    <tr>
                      <td colSpan={6} className="px-5 py-12 text-center text-muted-foreground">
                        No compliance reports found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Rule Violations</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <ul className="divide-y divide-border">
              {violations?.map((v: any) => (
                <li key={v.id} className="flex items-center gap-3 px-5 py-3.5">
                  <Badge
                    variant={v.severity === "high" ? "destructive" : v.severity === "medium" ? "warning" : "success"}
                    className="shrink-0"
                  >
                    {v.severity}
                  </Badge>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">{v.rule}</p>
                    <p className="text-xs text-muted-foreground">{v.shipmentRef}</p>
                  </div>
                  <Button variant="ghost" size="sm">
                    View
                  </Button>
                </li>
              ))}
              {(!violations || violations.length === 0) && (
                <li className="px-5 py-12 text-center text-muted-foreground">
                  No violations found.
                </li>
              )}
            </ul>
          </CardContent>
        </Card>
      </div>

      {/* Compliance Checks for a sample shipment */}
      <Card>
        <CardHeader>
          <CardTitle>Sample Shipment Compliance Checks</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground mb-4">Showing checks for TCA-2025-1042 (Kariba Foods)</p>
          <ul className="divide-y divide-border">
            {shipments[0]?.checks?.map((c: any) => {
              const { icon: CheckI, cls } = checkIcon[c.status]
              return (
                <li key={c.id} className="flex gap-3 px-2 py-3.5">
                  <CheckI className={`mt-0.5 size-4 shrink-0 ${cls}`} />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-foreground">{c.rule}</p>
                    <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">{c.detail}</p>
                  </div>
                  <Badge
                    variant={c.status === "pass" ? "success" : c.status === "warning" ? "warning" : "destructive"}
                  >
                    {c.status}
                  </Badge>
                </li>
              )
            })}
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}