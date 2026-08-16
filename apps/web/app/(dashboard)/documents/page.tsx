"use client"

import { FileText, Upload, Download, Search, Filter } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { formatDate, formatCurrency } from "@/lib/utils"
import { useDocuments } from "@/lib/hooks"

export default function DocumentsPage() {
  const { data: documentsResponse, isLoading } = useDocuments()
  const documents = documentsResponse?.items || []

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-foreground">Documents</h1>
        <Button className="gap-2">
          <Upload className="size-4" />
          Upload Document
        </Button>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-3 rounded-2xl border border-border bg-card p-4 lg:flex-row lg:items-center">
        <div className="relative flex-1 max-w-md">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search documents..."
            className="h-10 pl-9 pr-3"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="size-4 text-muted-foreground" />
          <select className="h-10 rounded-xl border border-border bg-background px-3 text-sm outline-none">
            <option>All types</option>
            <option>Commercial Invoice</option>
            <option>Bill of Lading</option>
            <option>Packing List</option>
            <option>Certificate of Origin</option>
          </select>
        </div>
      </div>

      {/* Document Table */}
      <Card>
        <CardHeader className="pb-0">
          <CardTitle>All Documents ({documents.length})</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="p-5 animate-pulse">
              <div className="h-4 bg-muted rounded w-1/4 mb-4" />
              <div className="h-64 bg-muted rounded" />
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[800px] text-sm">
                <thead>
                  <tr className="border-b border-border text-left text-xs uppercase tracking-wide text-muted-foreground">
                    <th className="px-5 py-3 font-medium">Document</th>
                    <th className="px-5 py-3 font-medium">Shipment</th>
                    <th className="px-5 py-3 font-medium">Type</th>
                    <th className="px-5 py-3 font-medium">Status</th>
                    <th className="px-5 py-3 font-medium">Confidence</th>
                    <th className="px-5 py-3 font-medium">Size</th>
                    <th className="px-5 py-3 font-medium">Uploaded</th>
                    <th className="px-5 py-3 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {documents.map((d: any) => (
                    <tr key={d.id} className="hover:bg-muted/50">
                      <td className="px-5 py-3.5 font-medium text-foreground">{d.file_name || d.name}</td>
                      <td className="px-5 py-3.5 text-muted-foreground">{d.shipmentRef || d.shipment_id}</td>
                      <td className="px-5 py-3.5">
                        <Badge variant="secondary">{d.document_type?.replace("_", " ") || d.type?.replace("_", " ")}</Badge>
                      </td>
                      <td className="px-5 py-3.5">
                        <Badge
                          variant={
                            d.extraction_status === "completed" || d.status === "extracted"
                              ? "success"
                              : d.extraction_status === "processing" || d.status === "processing"
                                ? "info"
                                : d.extraction_status === "review_required" || d.status === "review_required"
                                  ? "warning"
                                  : "destructive"
                          }
                        >
                          {d.extraction_status?.replace("_", " ") || d.status?.replace("_", " ")}
                        </Badge>
                      </td>
                      <td className="px-5 py-3.5 text-muted-foreground">
                        {d.confidence ? `${Math.round(d.confidence * 100)}%` : "—"}
                      </td>
                      <td className="px-5 py-3.5 text-muted-foreground">{d.file_size ? `${Math.round(d.file_size / 1024)} KB` : d.size}</td>
                      <td className="px-5 py-3.5 text-muted-foreground">{d.created_at ? formatDate(d.created_at) : formatDate(d.uploadedAt)}</td>
                      <td className="px-5 py-3.5">
                        <div className="flex items-center gap-2">
                          <Button variant="ghost" size="icon" className="h-8 w-8">
                            <Download className="size-4" />
                          </Button>
                          <Button variant="ghost" size="icon" className="h-8 w-8">
                            <FileText className="size-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {documents.length === 0 && (
                    <tr>
                      <td colSpan={8} className="px-5 py-12 text-center text-muted-foreground">
                        No documents found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}