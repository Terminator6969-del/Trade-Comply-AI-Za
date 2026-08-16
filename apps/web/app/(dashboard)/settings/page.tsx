"use client"

import { useState } from "react"
import { User, Users, Key, CreditCard, Bell, Shield, Save, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { useAuth, useOrganization } from "@/lib/hooks"

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("general")
  const [saving, setSaving] = useState(false)
  const { data: user } = useAuth()
  const { data: organization } = useOrganization()

  const handleSave = async () => {
    setSaving(true)
    await new Promise((r) => setTimeout(r, 1000))
    setSaving(false)
  }

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold text-foreground">Settings</h1>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="general"><User className="mr-2 size-4" /> Profile</TabsTrigger>
          <TabsTrigger value="organization"><Users className="mr-2 size-4" /> Organization</TabsTrigger>
          <TabsTrigger value="notifications"><Bell className="mr-2 size-4" /> Notifications</TabsTrigger>
          <TabsTrigger value="api"><Key className="mr-2 size-4" /> API Keys</TabsTrigger>
          <TabsTrigger value="billing"><CreditCard className="mr-2 size-4" /> Billing</TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="mt-6 flex flex-col gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Profile Information</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4 md:grid-cols-2">
              <div>
                <Label htmlFor="fullName">Full Name</Label>
                <Input id="fullName" defaultValue={user?.full_name || "Nomsa Mbeki"} />
              </div>
              <div>
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" defaultValue={user?.email || "nomsa@tradecomply.ai"} />
              </div>
              <div>
                <Label htmlFor="role">Role</Label>
                <Input id="role" defaultValue="Compliance Lead" disabled />
              </div>
              <div>
                <Label htmlFor="phone">Phone</Label>
                <Input id="phone" placeholder="+27 82 123 4567" />
              </div>
              <div className="md:col-span-2">
                <Label htmlFor="bio">Bio</Label>
                <Input id="bio" placeholder="Tell us about yourself..." />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Security</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button variant="outline" className="w-fit">Change Password</Button>
              <Button variant="outline" className="w-fit">Enable 2FA</Button>
              <Button variant="outline" className="w-fit">Manage Sessions</Button>
            </CardContent>
          </Card>

          <Button onClick={handleSave} disabled={saving} className="w-fit">
            {saving ? <Loader2 className="mr-2 size-4 animate-spin" /> : <Save className="mr-2 size-4" />}
            Save Changes
          </Button>
        </TabsContent>

        <TabsContent value="organization" className="mt-6 flex flex-col gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Organization Details</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4 md:grid-cols-2">
              <div>
                <Label htmlFor="orgName">Organization Name</Label>
                <Input id="orgName" defaultValue={organization?.name || "TradeComply Demo"} />
              </div>
              <div>
                <Label htmlFor="orgSlug">Slug</Label>
                <Input id="orgSlug" defaultValue={organization?.slug || "tradecomply-demo"} disabled />
              </div>
              <div>
                <Label htmlFor="plan">Plan</Label>
                <Input id="plan" defaultValue={organization?.plan || "Pro"} disabled />
              </div>
              <div>
                <Label htmlFor="vatNumber">VAT Number</Label>
                <Input id="vatNumber" placeholder="4990123456" />
              </div>
              <div className="md:col-span-2">
                <Label htmlFor="address">Address</Label>
                <Input id="address" placeholder="123 Main St, Johannesburg, 2000" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Team Members</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[
                  { name: "Nomsa Mbeki", email: "nomsa@tradecomply.ai", role: "Owner", status: "active" },
                  { name: "Thabo Nkosi", email: "thabo@karibafoods.co.za", role: "Admin", status: "active" },
                  { name: "Fatima Adams", email: "fatima@seaboardclearing.co.za", role: "Member", status: "pending" },
                ].map((m, i) => (
                  <div key={i} className="flex items-center justify-between p-3 rounded-lg border border-border">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground text-sm font-semibold">
                        {m.name.split(" ").map((n) => n[0]).join("")}
                      </div>
                      <div>
                        <p className="font-medium text-foreground">{m.name}</p>
                        <p className="text-xs text-muted-foreground">{m.email}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Badge variant="secondary">{m.role}</Badge>
                      <Badge variant={m.status === "active" ? "success" : "warning"}>{m.status}</Badge>
                    </div>
                  </div>
                ))}
              </div>
              <Button variant="outline" className="mt-4 w-fit gap-2">
                <User className="size-4" />
                Invite Member
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="mt-6 flex flex-col gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {[
                { label: "Shipment status changes", description: "Get notified when shipment status updates" },
                { label: "Compliance alerts", description: "Critical compliance violations and warnings" },
                { label: "Document extraction complete", description: "When AI finishes processing documents" },
                { label: "Weekly compliance digest", description: "Summary email every Monday" },
                { label: "Billing reminders", description: "Invoice due and payment notifications" },
              ].map((n, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-foreground">{n.label}</p>
                    <p className="text-xs text-muted-foreground">{n.description}</p>
                  </div>
                  <Switch defaultChecked />
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="api" className="mt-6 flex flex-col gap-6">
          <Card>
            <CardHeader>
              <CardTitle>API Keys</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">Manage your API keys for programmatic access.</p>
              <div className="space-y-3">
                {[
                  { name: "Production Key", prefix: "tc_live_", created: "2025-01-15", lastUsed: "2 hours ago" },
                  { name: "Development Key", prefix: "tc_test_", created: "2025-02-20", lastUsed: "3 days ago" },
                ].map((k, i) => (
                  <div key={i} className="flex items-center justify-between p-3 rounded-lg border border-border">
                    <div>
                      <p className="font-medium text-foreground">{k.name}</p>
                      <p className="text-xs text-muted-foreground font-mono">{k.prefix}••••••••</p>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <span>Created: {k.created}</span>
                      <span>•</span>
                      <span>Last used: {k.lastUsed}</span>
                    </div>
                  </div>
                ))}
              </div>
              <Button variant="outline" className="w-fit gap-2">
                <Key className="size-4" />
                Generate New Key
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="billing" className="mt-6 flex flex-col gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Current Plan</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div className="rounded-xl border border-border bg-card p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-2xl font-bold text-foreground">Pro Plan</p>
                    <p className="text-sm text-muted-foreground">R12,500 / month</p>
                  </div>
                  <Badge variant="success">Active</Badge>
                </div>
                <div className="mt-4 grid grid-cols-3 gap-4 text-center">
                  <div className="rounded-lg bg-muted p-4">
                    <p className="text-2xl font-bold text-foreground">50</p>
                    <p className="text-xs text-muted-foreground">Shipments/month</p>
                  </div>
                  <div className="rounded-lg bg-muted p-4">
                    <p className="text-2xl font-bold text-foreground">Unlimited</p>
                    <p className="text-xs text-muted-foreground">Documents</p>
                  </div>
                  <div className="rounded-lg bg-muted p-4">
                    <p className="text-2xl font-bold text-foreground">10</p>
                    <p className="text-xs text-muted-foreground">Team members</p>
                  </div>
                </div>
              </div>
              <Button variant="outline" className="w-fit">Manage Subscription</Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Billing History</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[
                  { date: "2025-08-01", amount: "R12,500.00", status: "Paid", invoice: "INV-2025-001" },
                  { date: "2025-07-01", amount: "R12,500.00", status: "Paid", invoice: "INV-2025-002" },
                  { date: "2025-06-01", amount: "R12,500.00", status: "Paid", invoice: "INV-2025-003" },
                ].map((b, i) => (
                  <div key={i} className="flex items-center justify-between p-3 rounded-lg border border-border">
                    <div>
                      <p className="font-medium text-foreground">{b.invoice}</p>
                      <p className="text-xs text-muted-foreground">{b.date}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="font-medium text-foreground">{b.amount}</span>
                      <Badge variant={b.status === "Paid" ? "success" : "warning"}>{b.status}</Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}