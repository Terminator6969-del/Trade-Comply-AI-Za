"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  LayoutDashboard,
  Ship,
  FileText,
  ShieldCheck,
  Users,
  Calculator,
  Settings,
  Globe,
  LifeBuoy,
} from "lucide-react"
import { cn } from "@/lib/utils"

const mainNav = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/shipments", label: "Shipments", icon: Ship },
  { href: "/documents", label: "Documents", icon: FileText },
  { href: "/compliance", label: "Compliance", icon: ShieldCheck },
  { href: "/parties", label: "Parties", icon: Users },
  { href: "/tariffs", label: "Tariffs", icon: Calculator },
]

const generalNav = [
  { href: "/settings", label: "Settings", icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  const renderLink = (item: (typeof mainNav)[number]) => {
    const active = pathname === item.href || pathname.startsWith(item.href + "/")
    const Icon = item.icon
    return (
      <Link
        key={item.href}
        href={item.href}
        className={cn(
          "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors",
          active
            ? "bg-primary/10 text-primary"
            : "text-muted-foreground hover:bg-primary/5 hover:text-primary",
        )}
      >
        <Icon className="size-[18px]" strokeWidth={active ? 2.4 : 2} />
        {item.label}
      </Link>
    )
  }

  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-border bg-background lg:flex">
      <div className="flex h-16 items-center gap-2.5 px-6 border-b border-border">
        <div className="flex size-9 items-center justify-center rounded-xl bg-primary text-primary-foreground">
          <Globe className="size-5" />
        </div>
        <div className="leading-tight">
          <p className="text-sm font-bold text-foreground">TradeComply</p>
          <p className="text-[11px] font-medium text-muted-foreground">AI South Africa</p>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-1 px-4 py-4">
        <p className="px-3 pb-2 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
          Menu
        </p>
        {mainNav.map(renderLink)}

        <p className="px-3 pb-2 pt-5 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
          General
        </p>
        {generalNav.map(renderLink)}
      </nav>

      <div className="m-4 rounded-2xl bg-primary p-4 text-primary-foreground">
        <div className="flex items-center gap-2">
          <LifeBuoy className="size-5" />
          <p className="text-sm font-semibold">Need help?</p>
        </div>
        <p className="mt-1.5 text-xs text-primary-foreground/80">
          Talk to our compliance specialists about SARS customs rulings.
        </p>
        <button className="mt-3 w-full rounded-lg bg-primary-foreground/15 py-2 text-xs font-semibold transition-colors hover:bg-primary-foreground/25">
          Contact support
        </button>
      </div>
    </aside>
  )
}
