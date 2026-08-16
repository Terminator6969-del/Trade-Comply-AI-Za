import { AnimatePresence, motion } from "framer-motion";
import { Bell, Menu, Moon, Search, Sparkles, Sun } from "lucide-react";
import { useEffect, useRef } from "react";
import { notifications } from "../lib/data";
import { useApp } from "../lib/store";
import { clsx } from "../lib/format";

export function TopBar() {
  const {
    dark,
    toggleDark,
    setSidebar,
    notifOpen,
    setNotifOpen,
    setSearchOpen,
    setCopilotOpen,
  } = useApp();
  const box = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onDoc = (e: MouseEvent) => {
      if (box.current && !box.current.contains(e.target as Node)) setNotifOpen(false);
    };
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, [setNotifOpen]);

  const unread = notifications.filter((n) => n.unread).length;

  return (
    <header className="sticky top-0 z-20 flex items-center gap-3 border-b border-[#e6eae2]/70 bg-[#f4f5f0]/62 px-4 py-3 backdrop-blur-2xl dark:border-white/8 dark:bg-[#0a1c18]/62 lg:px-8">
      <button
        className="rounded-xl p-2 text-[#0F2B24] hover:bg-white dark:text-white dark:hover:bg-white/8 lg:hidden"
        onClick={() => setSidebar(true)}
        aria-label="Open menu"
      >
        <Menu className="h-5 w-5" />
      </button>

      <button
        onClick={() => setSearchOpen(true)}
        className="relative flex h-11 flex-1 items-center rounded-full border border-[#e2e7de] bg-white/80 pl-10 pr-16 text-left text-[13.5px] text-[#93a098] shadow-sm transition hover:border-[#cfd7c8] dark:border-white/10 dark:bg-white/5"
      >
        <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-[#8a968e]" />
        Search shipments, HS codes, parties…
        <kbd className="pointer-events-none absolute right-3 top-1/2 hidden -translate-y-1/2 rounded-md border border-[#e2e7de] bg-[#f6f7f3] px-1.5 py-0.5 text-[10px] font-medium text-[#7d8c84] sm:inline-block dark:border-white/10 dark:bg-white/5">
          ⌘K
        </kbd>
      </button>

      <button
        onClick={() => setCopilotOpen(true)}
        className="hidden h-11 items-center gap-2 rounded-full border border-[#e2e7de] bg-white px-3.5 text-[12.5px] font-semibold text-[#0F2B24] shadow-sm transition hover:bg-[#f4f6f0] md:inline-flex dark:border-white/10 dark:bg-white/5 dark:text-[#B7EE55]"
      >
        <Sparkles className="h-3.5 w-3.5" />
        Copilot
      </button>

      <button
        onClick={toggleDark}
        className="flex h-11 w-11 items-center justify-center rounded-full border border-[#e2e7de] bg-white text-[#0F2B24] shadow-sm transition hover:bg-[#f4f6f0] dark:border-white/10 dark:bg-white/5 dark:text-[#B7EE55]"
        aria-label="Toggle dark mode"
      >
        {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
      </button>

      <div className="relative" ref={box}>
        <button
          onClick={() => setNotifOpen(!notifOpen)}
          className="relative flex h-11 w-11 items-center justify-center rounded-full border border-[#e2e7de] bg-white text-[#0F2B24] shadow-sm hover:bg-[#f4f6f0] dark:border-white/10 dark:bg-white/5 dark:text-white"
          aria-label="Notifications"
        >
          <Bell className="h-4 w-4" />
          {unread > 0 && (
            <span className="pulse-dot absolute right-2.5 top-2.5 h-2 w-2 rounded-full bg-rose-500 ring-2 ring-white dark:ring-[#0a1c18]" />
          )}
        </button>
        <AnimatePresence>
          {notifOpen && (
            <motion.div
              initial={{ opacity: 0, y: 8, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 6 }}
              transition={{ duration: 0.18 }}
              className="absolute right-0 mt-2 w-[340px] overflow-hidden rounded-2xl border border-[#e2e7de] bg-white/95 shadow-xl backdrop-blur-xl dark:border-white/10 dark:bg-[#122821]/95"
            >
              <div className="flex items-center justify-between border-b border-[#eef1ea] px-4 py-3 dark:border-white/8">
                <p className="text-sm font-semibold text-[#12211c] dark:text-white">Notifications</p>
                <span className="text-[11px] text-[#8a968e]">{unread} unread</span>
              </div>
              <ul>
                {notifications.map((n) => (
                  <li
                    key={n.id}
                    className={clsx(
                      "border-b border-[#f1f3ee] px-4 py-3 last:border-0 dark:border-white/5",
                      n.unread && "bg-[#f7faf3] dark:bg-white/4",
                    )}
                  >
                    <p className="text-[13px] font-semibold text-[#12211c] dark:text-white">{n.title}</p>
                    <p className="mt-0.5 text-[12px] leading-snug text-[#6b7a72]">{n.body}</p>
                    <p className="mt-1 text-[11px] text-[#9aa59d]">{n.time}</p>
                  </li>
                ))}
              </ul>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div className="hidden items-center gap-2.5 pl-1 sm:flex">
        <img src="/images/thandi.jpg" alt="" className="h-10 w-10 rounded-full object-cover ring-2 ring-white dark:ring-white/10" />
        <div className="hidden leading-tight md:block">
          <p className="text-[13px] font-semibold text-[#12211c] dark:text-white">Thandi Mokoena</p>
          <p className="text-[11px] text-[#7d8c84]">thandi@tradecomply.ai</p>
        </div>
      </div>
    </header>
  );
}
