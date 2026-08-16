"use client"

import { useState } from "react"
import { Calculator, Search, Filter, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useTariffs, useCalculateDuty } from "@/lib/hooks"

export default function TariffsPage() {
  const { data: tariffs, isLoading } = useTariffs()
  const calculateDuty = useCalculateDuty()

  const [hsCode, setHsCode] = useState("")
  const [value, setValue] = useState("")
  const [quantity, setQuantity] = useState("1")
  const [dutyResult, setDutyResult] = useState<any>(null)

  const handleCalculate = async () => {
    if (!hsCode || !value) return
    try {
      const result = await calculateDuty.mutateAsync({
        hs_code: hsCode,
        value: parseFloat(value),
        quantity: parseInt(quantity),
        origin_country: "CN",
      })
      setDutyResult(result)
    } catch (error) {
      console.error("Failed to calculate duty:", error)
    }
  }

  if (isLoading) {
    return (
      <div className="flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-foreground">Tariffs</h1>
          <Loader2 className="size-4 text-primary animate-spin" />
        </div>
        <Card className="animate-pulse">
          <CardHeader>
            <CardTitle>Loading...</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 bg-muted rounded" />
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-foreground">Tariffs</h1>
        <div className="flex items-center gap-2">
          <Button variant="outline" className="gap-2">
            <Filter className="size-4" />
            Filters
          </Button>
          <Button className="gap-2">
            <Calculator className="size-4" />
            Duty Calculator
          </Button>
        </div>
      </div>

      {/* Search */}
      <div className="flex flex-col gap-3 rounded-2xl border border-border bg-card p-4 lg:flex-row lg:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search HS codes, descriptions..."
            className="h-10 pl-9 pr-3"
          />
        </div>
        <div className="flex items-center gap-2">
          <select className="h-10 rounded-xl border border-border bg-background px-3 text-sm outline-none">
            <option>All chapters</option>
            <option>Chapter 08 - Edible fruit</option>
            <option>Chapter 52 - Cotton</option>
            <option>Chapter 64 - Footwear</option>
            <option>Chapter 85 - Electrical machinery</option>
          </select>
        </div>
      </div>

      {/* Tariff Table */}
      <Card>
        <CardHeader className="pb-0">
          <CardTitle>SARS Tariff Schedule ({tariffs?.length || 0} entries)</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[800px] text-sm">
              <thead>
                <tr className="border-b border-border text-left text-xs uppercase tracking-wide text-muted-foreground">
                  <th className="px-5 py-3 font-medium">HS Code</th>
                  <th className="px-5 py-3 font-medium">Description</th>
                  <th className="px-5 py-3 font-medium">Duty Rate</th>
                  <th className="px-5 py-3 font-medium">VAT</th>
                  <th className="px-5 py-3 font-medium">Unit</th>
                  <th className="px-5 py-3 font-medium">Restrictions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {tariffs?.map((t: any) => (
                  <tr key={t.hsCode || t.id} className="hover:bg-muted/50">
                    <td className="px-5 py-3.5 font-mono font-medium text-foreground">{t.hsCode || t.hs_code}</td>
                    <td className="px-5 py-3.5 text-foreground">{t.description}</td>
                    <td className="px-5 py-3.5 font-medium text-foreground">{t.dutyRate || t.duty_rate}%</td>
                    <td className="px-5 py-3.5 text-muted-foreground">{t.vat}%</td>
                    <td className="px-5 py-3.5 text-muted-foreground">{t.unit}</td>
                    <td className="px-5 py-3.5">
                      {t.restrictions?.length > 0 ? (
                        <div className="flex flex-wrap gap-1">
                          {t.restrictions.map((r: string, i: number) => (
                            <Badge key={i} variant="outline" className="text-xs">
                              {r}
                            </Badge>
                          ))}
                        </div>
                      ) : (
                        <span className="text-muted-foreground">—</span>
                      )}
                    </td>
                  </tr>
                ))}
                {(!tariffs || tariffs.length === 0) && (
                  <tr>
                    <td colSpan={6} className="px-5 py-12 text-center text-muted-foreground">
                      No tariff entries found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Duty Calculator */}
      <Card>
        <CardHeader>
          <CardTitle>Duty Calculator</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="mb-1.5 block text-xs font-medium text-foreground">HS Code</label>
              <Input placeholder="e.g., 8507.60" value={hsCode} onChange={(e) => setHsCode(e.target.value)} />
            </div>
            <div>
              <label className="mb-1.5 block text-xs font-medium text-foreground">Value (ZAR)</label>
              <Input type="number" placeholder="100000" value={value} onChange={(e) => setValue(e.target.value)} />
            </div>
            <div>
              <label className="mb-1.5 block text-xs font-medium text-foreground">Quantity</label>
              <Input type="number" placeholder="1" value={quantity} onChange={(e) => setQuantity(e.target.value)} />
            </div>
          </div>
          <div className="mt-4 flex items-center gap-4">
            <Button className="gap-2" onClick={handleCalculate} disabled={calculateDuty.isPending}>
              {calculateDuty.isPending ? <Loader2 className="size-4 animate-spin" /> : <Calculator className="size-4" />}
              Calculate
            </Button>
            {dutyResult && (
              <div className="text-sm text-muted-foreground">
                Estimated duty: <span className="font-medium text-foreground">R{dutyResult.duty?.toLocaleString() || "0.00"}</span> | VAT: <span className="font-medium text-foreground">R{dutyResult.vat?.toLocaleString() || "0.00"}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}