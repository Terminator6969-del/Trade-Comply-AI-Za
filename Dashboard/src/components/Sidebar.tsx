import { NavLink, useLocation } from "react-router-dom";
import {
  BarChart3,
  BookOpen,
  ChevronDown,
  FileStack,
  LayoutDashboard,
  Settings,
  ShieldCheck,
  Ship,
  Users,
  Sparkles,
} from "lucide-react";
import { workspaces } from "../lib/data";
import { useApp } from "../lib/store";
import { clsx } from "../lib/format";
import { useState } from "react";
import { Logo } from "./Logo";

const nav = [
  { to: "/dashboard", label: "Overview", icon: LayoutDashboard },
  { to: "/shipments", label: "Shipments", icon: Ship, badge: 14 },
  { to: "/documents", label: "Documents", icon: FileStack },
  { to: "/compliance", label: "Compliance", icon: ShieldCheck },
  { to: "/parties", label: "Trade parties", icon: Users },
  { to: "/tariffs", label: "Tariffs & HS codes", icon: BookOpen },
];

export function Sidebar() {
  const { workspace, setWorkspace, sidebarOpen, setSidebar, setCopilotOpen } = useApp();
  const [openWs, setOpenWs] = useState(false);
  const loc = useLocation();
  const current = workspaces.find((w) => w.id === workspace) ?? workspaces[0];

  return (
    <>
      {sidebarOpen && (
        <button
          className="fixed inset-0 z-30 bg-[#0F2B24]/30 backdrop-blur-[2px] lg:hidden"
          onClick={() => setSidebar(false)}
          aria-label="Close menu"
        />
      )}
      <aside
        className={clsx(
          "fixed inset-y-0 left-0 z-40 flex w-[260px] flex-col border-r border-[#e6eae2]/80 bg-[#f7f8f4]/78 px-4 py-5 backdrop-blur-2xl transition-transform duration-300 dark:border-white/8 dark:bg-[#0c1f1a]/90 lg:static lg:translate-x-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex items-center gap-2.5 px-1">
          <Logo size={34} />
          <div className="min-w-0">
            <p className="truncate text-[15px] font-bold tracking-tight text-[#0F2B24] dark:text-white">
              TradeComply
            </p>
            <p className="text-[10px] font-medium uppercase tracking-[0.14em] text-[#7d8c84]">
              South Africa
            </p>
          </div>
        </div>

        <div className="relative mt-5">
          <button
            onClick={() => setOpenWs((v) => !v)}
            className="flex w-full items-center justify-between rounded-xl border border-[#e2e7de] bg-white px-3 py-2 text-left shadow-sm dark:border-white/10 dark:bg-white/5"
          >
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-wider text-[#8a968e]">Workspace</p>
              <p className="text-[13px] font-semibold text-[#12211c] dark:text-white">{current.name}</p>
            </div>
            <ChevronDown className="h-4 w-4 text-[#6b7a72]" />
          </button>
          {openWs && (
            <div className="absolute left-0 right-0 z-20 mt-1 overflow-hidden rounded-xl border border-[#e2e7de] bg-white py-1 shadow-lg dark:border-white/10 dark:bg-[#132821]">
              {workspaces.map((w) => (
                <button
                  key={w.id}
                  onClick={() => {
                    setWorkspace(w.id);
                    setOpenWs(false);
                  }}
                  className={clsx(
                    "block w-full px-3 py-2 text-left text-[13px] hover:bg-[#f3f6ef] dark:hover:bg-white/5",
                    w.id === workspace ? "font-semibold text-[#0F2B24] dark:text-[#B7EE55]" : "text-[#3d4d46] dark:text-[#d5ddd6]",
                  )}
                >
                  <span className="block">{w.name}</span>
                  <span className="text-[11px] font-normal text-[#8a968e]">{w.region}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        <p className="mt-6 px-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-[#9aa59d]">Menu</p>
        <nav className="mt-2 flex flex-1 flex-col gap-0.5">
          {nav.map((item) => {
            const Icon = item.icon;
            const active = item.to === "/dashboard" ? loc.pathname === "/dashboard" : loc.pathname.startsWith(item.to);
            return (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={() => setSidebar(false)}
                className={clsx(
                  "group relative flex items-center gap-2.5 rounded-xl px-3 py-2 text-[13.5px] font-medium transition-colors",
                  active
                    ? "bg-white text-[#0F2B24] shadow-sm dark:bg-white/8 dark:text-white"
                    : "text-[#5c6b64] hover:bg-white/70 hover:text-[#0F2B24] dark:text-[#9eaea6] dark:hover:bg-white/5 dark:hover:text-white",
                )}
              >
                {active && (
                  <span className="absolute left-0 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-r-full bg-[#A3E635]" />
                )}
                <Icon className={clsx("h-[18px] w-[18px]", active ? "text-[#0F2B24] dark:text-[#B7EE55]" : "")} />
                <span className="flex-1">{item.label}</span>
                {item.badge ? (
                  <span className="rounded-full bg-[#0F2B24] px-1.5 py-px text-[10px] font-semibold text-[#B7EE55] dark:bg-[#A3E635] dark:text-[#0F2B24]">
                    {item.badge}
                  </span>
                ) : null}
              </NavLink>
            );
          })}

          <p className="mt-5 px-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-[#9aa59d]">General</p>
          <NavLink
            to="/settings"
            onClick={() => setSidebar(false)}
            className={({ isActive }) =>
              clsx(
                "mt-1 flex items-center gap-2.5 rounded-xl px-3 py-2 text-[13.5px] font-medium",
                isActive
                  ? "bg-white text-[#0F2B24] shadow-sm dark:bg-white/8 dark:text-white"
                  : "text-[#5c6b64] hover:bg-white/70 dark:text-[#9eaea6] dark:hover:bg-white/5",
              )
            }
          >
            <Settings className="h-[18px] w-[18px]" />
            Settings
          </NavLink>
        </nav>

        <div className="relative mt-4 overflow-hidden rounded-2xl bg-[#0F2B24] p-4 text-white shadow-[0_10px_28px_rgba(15,43,36,0.18)]">
          <img
            src="/images/promo-waves.png"
            alt=""
            className="absolute inset-0 h-full w-full object-cover opacity-70"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[#0F2B24] via-[#0F2B24]/70 to-transparent" />
          <div className="relative">
            <div className="mb-2 inline-flex items-center gap-1 rounded-full bg-[#A3E635]/15 px-2 py-0.5 text-[10px] font-semibold text-[#B7EE55]">
              <Sparkles className="h-3 w-3" />
              AI copilot
            </div>
            <p className="text-[13px] font-semibold leading-snug">Classify HS codes in seconds</p>
            <p className="mt-1 text-[11px] leading-relaxed text-white/70">
              Ask the model to draft SAD500 lines from a commercial invoice.
            </p>
            <button
              onClick={() => {
                setCopilotOpen(true);
                setSidebar(false);
              }}
              className="mt-3 w-full rounded-full bg-[#A3E635] px-3 py-1.5 text-[12px] font-semibold text-[#0F2B24] transition hover:bg-[#B7EE55]"
            >
              Open copilot
            </button>
          </div>
        </div>

        <div className="mt-3 flex items-center gap-2.5 rounded-xl px-1 py-1">
          <img src="/images/thandi.jpg" alt="" className="h-8 w-8 rounded-full object-cover" />
          <div className="min-w-0">
            <p className="truncate text-[13px] font-semibold text-[#12211c] dark:text-white">Thandi Mokoena</p>
            <p className="truncate text-[11px] text-[#7d8c84]">Cape Town Hub</p>
          </div>
          <BarChart3 className="ml-auto h-4 w-4 text-[#9aa59d]" />
        </div>
      </aside>
    </>
  );
}
