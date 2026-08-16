"use client"

import { Search, Bell, Mail } from "lucide-react"
import { cn } from "@/lib/utils"

export function Header() {
  return (
    <header className="sticky top-0 z-20 flex h-16 items-center gap-4 border-b border-border bg-background/80 px-4 backdrop-blur md:px-8">
      <div className="relative w-full max-w-md">
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          type="search"
          placeholder="Search shipments, HS codes, parties..."
          aria-label="Search"
          className="h-10 w-full rounded-xl border border-border bg-card pl-9 pr-16 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-primary/40 focus:ring-2 focus:ring-primary/15"
        />
        <kbd className="absolute right-3 top-1/2 hidden -translate-y-1/2 rounded-md border border-border bg-muted px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground sm:block">
          ⌘K
        </kbd>
      </div>

      <div className="ml-auto flex items-center gap-1.5">
        <button
          aria-label="Messages"
          className="flex size-10 items-center justify-center rounded-xl text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
        >
          <Mail className="size-[18px]" />
        </button>
        <button
          aria-label="Notifications"
          className="relative flex size-10 items-center justify-center rounded-xl text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
        >
          <Bell className="size-[18px]" />
          <span className="absolute right-2.5 top-2.5 size-2 rounded-full bg-primary ring-2 ring-background" />
        </button>
        <div className="ml-2 flex items-center gap-3 border-l border-border pl-3">
          <div className="w-9 h-9 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-semibold">
            NM
          </div>
          <div className="hidden leading-tight sm:block">
            <p className="text-sm font-medium text-foreground">Nomsa Mbeki</p>
            <p className="text-xs text-muted-foreground">Compliance Lead</p>
          </div>
        </div>
      </div>
    </header>
  )
}
