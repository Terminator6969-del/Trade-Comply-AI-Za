"use client"

import { Users, Building2, Truck, Plus, Search, MoreHorizontal, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useParties } from "@/lib/hooks"

export default function PartiesPage() {
  const { data: partiesResponse, isLoading } = useParties()
  const parties = partiesResponse || []

  if (isLoading) {
    return (
      <div className="flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-foreground">Parties</h1>
          <Loader2 className="size-4 text-primary animate-spin" />
        </div>
        <Card className="animate-pulse">
          <CardHeader className="pb-0">
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
        <h1 className="text-2xl font-bold text-foreground">Parties</h1>
        <Button className="gap-2">
          <Plus className="size-4" />
          Add Party
        </Button>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-3 rounded-2xl border border-border bg-card p-4 lg:flex-row lg:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search parties..."
            className="h-10 pl-9 pr-3"
          />
        </div>
        <div className="flex items-center gap-2">
          <select className="h-10 rounded-xl border border-border bg-background px-3 text-sm outline-none">
            <option>All types</option>
            <option>Importers</option>
            <option>Suppliers</option>
            <option>Clearing Agents</option>
          </select>
        </div>
      </div>

      {/* Parties Table */}
      <Card>
        <CardHeader className="pb-0">
          <CardTitle>All Parties ({parties.length})</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[700px] text-sm">
              <thead>
                <tr className="border-b border-border text-left text-xs uppercase tracking-wide text-muted-foreground">
                  <th className="px-5 py-3 font-medium">Name</th>
                  <th className="px-5 py-3 font-medium">Type</th>
                  <th className="px-5 py-3 font-medium">Country</th>
                  <th className="px-5 py-3 font-medium">Tax ID</th>
                  <th className="px-5 py-3 font-medium">Contact</th>
                  <th className="px-5 py-3 font-medium">Active Shipments</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {parties.map((p: any) => {
                  const typeIcon = p.type === "importer" ? Building2 : p.type === "supplier" ? Building2 : Truck
                  return (
                    <tr key={p.id} className="hover:bg-muted/50">
                      <td className="px-5 py-3.5">
                        <div className="flex items-center gap-3">
                          <div className="flex size-8 items-center justify-center rounded-lg bg-muted text-muted-foreground">
                            <typeIcon className="size-4" />
                          </div>
                          <span className="font-medium text-foreground">{p.name}</span>
                        </div>
                      </td>
                      <td className="px-5 py-3.5">
                        <Badge variant="secondary">{p.type}</Badge>
                      </td>
                      <td className="px-5 py-3.5 text-muted-foreground">{p.country}</td>
                      <td className="px-5 py-3.5 font-mono text-xs text-muted-foreground">{p.taxId || p.registration_number}</td>
                      <td className="px-5 py-3.5 text-foreground">{p.contact || p.contact_person}</td>
                      <td className="px-5 py-3.5 text-muted-foreground">{p.activeShipments || 0}</td>
                      <td className="px-5 py-3.5">
                        <Badge variant={p.status === "active" ? "success" : "secondary"}>
                          {p.status}
                        </Badge>
                      </td>
                      <td className="px-5 py-3.5">
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <MoreHorizontal className="size-4" />
                        </Button>
                      </td>
                    </tr>
                  )
                })}
                {parties.length === 0 && (
                  <tr>
                    <td colSpan={8} className="px-5 py-12 text-center text-muted-foreground">
                      No parties found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}