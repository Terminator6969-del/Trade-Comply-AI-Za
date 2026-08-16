import { AnimatePresence, motion } from "framer-motion";
import { ArrowUpRight, BookOpen, FileStack, Search, Settings, ShieldCheck, Ship, Users } from "lucide-react";
import { useEffect, useMemo, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { hsCodes } from "../lib/data";
import { useApp } from "../lib/store";

const pages = [
  { label: "Overview", to: "/dashboard", hint: "Dashboard", icon: Search },
  { label: "Shipments", to: "/shipments", hint: "Live book", icon: Ship },
  { label: "Documents", to: "/documents", hint: "SAD500s & permits", icon: FileStack },
  { label: "Compliance", to: "/compliance", hint: "Control tower", icon: ShieldCheck },
  { label: "Trade parties", to: "/parties", hint: "Importers & brokers", icon: Users },
  { label: "Tariffs & HS codes", to: "/tariffs", hint: "SARS schedule", icon: BookOpen },
  { label: "Settings", to: "/settings", hint: "Workspace", icon: Settings },
];

export function CommandPalette() {
  const { searchOpen, setSearchOpen, query, setQuery, shipments, setModalOpen, setCopilotOpen } = useApp();
  const nav = useNavigate();
  const input = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setSearchOpen(!searchOpen);
      }
      if (e.key === "Escape") setSearchOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [searchOpen, setSearchOpen]);

  useEffect(() => {
    if (searchOpen) {
      setTimeout(() => input.current?.focus(), 40);
    }
  }, [searchOpen]);

  const q = query.trim().toLowerCase();

  const hits = useMemo(() => {
    const ship = shipments
      .filter(
        (s) =>
          !q ||
          s.id.toLowerCase().includes(q) ||
          s.company.toLowerCase().includes(q) ||
          s.origin.toLowerCase().includes(q) ||
          s.destination.toLowerCase().includes(q) ||
          s.hsCode.includes(q),
      )
      .slice(0, 5);
    const codes = hsCodes
      .filter((h) => !q || h.code.includes(q) || h.description.toLowerCase().includes(q))
      .slice(0, 3);
    const navItems = pages.filter((p) => !q || p.label.toLowerCase().includes(q));
    return { ship, codes, navItems };
  }, [q, shipments]);

  const go = (to: string) => {
    setSearchOpen(false);
    setQuery("");
    nav(to);
  };

  return (
    <AnimatePresence>
      {searchOpen && (
        <motion.div
          className="fixed inset-0 z-[70] flex items-start justify-center bg-[#0F2B24]/28 px-4 pt-[12vh] backdrop-blur-md"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setSearchOpen(false)}
        >
          <motion.div
            initial={{ opacity: 0, y: 14, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.98 }}
            transition={{ type: "spring", stiffness: 380, damping: 30 }}
            onClick={(e) => e.stopPropagation()}
            className="w-full max-w-[640px] overflow-hidden rounded-3xl border border-white/40 bg-[#f7f8f4]/90 shadow-[0_30px_80px_rgba(15,43,36,0.22)] backdrop-blur-2xl dark:border-white/10 dark:bg-[#10241e]/92"
          >
            <div className="flex items-center gap-3 border-b border-[#e6eae2] px-4 py-3.5 dark:border-white/8">
              <Search className="h-4 w-4 text-[#8a968e]" />
              <input
                ref={input}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search shipments, HS codes, pages…"
                className="h-8 flex-1 bg-transparent text-[14px] outline-none placeholder:text-[#93a098] dark:text-white"
              />
              <kbd className="rounded-md border border-[#e2e7de] bg-white px-1.5 py-0.5 text-[10px] font-medium text-[#7d8c84] dark:border-white/10 dark:bg-white/5">
                ESC
              </kbd>
            </div>

            <div className="max-h-[52vh] overflow-y-auto p-2">
              <p className="px-2 py-1.5 text-[10px] font-semibold uppercase tracking-[0.16em] text-[#9aa59d]">Pages</p>
              {hits.navItems.map((p) => {
                const Icon = p.icon;
                return (
                  <button
                    key={p.to}
                    onClick={() => go(p.to)}
                    className="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-left hover:bg-white dark:hover:bg-white/6"
                  >
                    <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#eef1ea] text-[#0F2B24] dark:bg-white/8 dark:text-[#B7EE55]">
                      <Icon className="h-4 w-4" />
                    </span>
                    <span className="flex-1">
                      <span className="block text-[13px] font-semibold">{p.label}</span>
                      <span className="text-[11px] text-[#8a968e]">{p.hint}</span>
                    </span>
                    <ArrowUpRight className="h-3.5 w-3.5 text-[#b0b8b2]" />
                  </button>
                );
              })}

              {hits.ship.length > 0 && (
                <>
                  <p className="mt-2 px-2 py-1.5 text-[10px] font-semibold uppercase tracking-[0.16em] text-[#9aa59d]">
                    Shipments
                  </p>
                  {hits.ship.map((s) => (
                    <button
                      key={s.id}
                      onClick={() => go(`/shipments/${s.id}`)}
                      className="flex w-full items-center justify-between rounded-xl px-3 py-2 text-left hover:bg-white dark:hover:bg-white/6"
                    >
                      <span>
                        <span className="block font-mono text-[12px] font-semibold text-[#0F2B24] dark:text-[#B7EE55]">
                          {s.id}
                        </span>
                        <span className="text-[12px] text-[#6b7a72]">
                          {s.company} · {s.origin} → {s.destination}
                        </span>
                      </span>
                      <span className="font-mono text-[11px] text-[#8a968e]">{s.hsCode}</span>
                    </button>
                  ))}
                </>
              )}

              {hits.codes.length > 0 && (
                <>
                  <p className="mt-2 px-2 py-1.5 text-[10px] font-semibold uppercase tracking-[0.16em] text-[#9aa59d]">
                    HS codes
                  </p>
                  {hits.codes.map((h) => (
                    <button
                      key={h.code}
                      onClick={() => go("/tariffs")}
                      className="flex w-full items-center justify-between rounded-xl px-3 py-2 text-left hover:bg-white dark:hover:bg-white/6"
                    >
                      <span>
                        <span className="block font-mono text-[12px] font-semibold">{h.code}</span>
                        <span className="text-[12px] text-[#6b7a72]">{h.description}</span>
                      </span>
                      <span className="text-[11px] text-[#8a968e]">{h.duty}</span>
                    </button>
                  ))}
                </>
              )}

              <div className="mt-2 grid grid-cols-2 gap-2 p-1">
                <button
                  onClick={() => {
                    setSearchOpen(false);
                    setModalOpen(true);
                  }}
                  className="rounded-xl bg-[#0F2B24] px-3 py-2.5 text-left text-[12px] font-semibold text-white dark:bg-[#A3E635] dark:text-[#0F2B24]"
                >
                  + New shipment
                </button>
                <button
                  onClick={() => {
                    setSearchOpen(false);
                    setCopilotOpen(true);
                  }}
                  className="rounded-xl bg-white px-3 py-2.5 text-left text-[12px] font-semibold ring-1 ring-[#e2e7de] dark:bg-white/5 dark:ring-white/10"
                >
                  Open AI copilot
                </button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
