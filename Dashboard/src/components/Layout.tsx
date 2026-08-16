import { AnimatePresence, motion } from "framer-motion";
import { Outlet, useLocation } from "react-router-dom";
import { CommandPalette } from "./CommandPalette";
import { Copilot } from "./Copilot";
import { NewShipmentModal } from "./NewShipmentModal";
import { Sidebar } from "./Sidebar";
import { Toast } from "./Toast";
import { TopBar } from "./TopBar";

export function Layout() {
  const location = useLocation();
  return (
    <div className="glow-spot relative min-h-screen overflow-hidden bg-[#dfe4d8] p-0 text-[#12211c] dark:bg-[#071411] dark:text-[#eef3ea] lg:p-4">
      <div className="orb floaty -left-24 top-24 h-64 w-64 bg-[#A3E635]/25 dark:bg-[#A3E635]/10" />
      <div className="orb -right-16 top-0 h-80 w-80 bg-[#0F2B24]/10 dark:bg-[#A3E635]/8" />
      <div className="noise" />

      <div className="relative mx-auto flex min-h-screen max-w-[1640px] overflow-hidden rounded-none border-0 border-white/50 bg-[#f3f4ef]/78 shadow-none backdrop-blur-xl dark:border-white/6 dark:bg-[#0b1915]/78 lg:min-h-[calc(100vh-32px)] lg:rounded-[32px] lg:border lg:shadow-[0_24px_80px_rgba(15,43,36,0.1)]">
        <Sidebar />
        <div className="flex min-w-0 flex-1 flex-col">
          <TopBar />
          <main className="flex-1 overflow-x-hidden px-4 py-5 lg:px-7 lg:py-6">
            <AnimatePresence mode="wait">
              <motion.div
                key={location.pathname}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
              >
                <Outlet />
              </motion.div>
            </AnimatePresence>
          </main>
        </div>
      </div>
      <NewShipmentModal />
      <CommandPalette />
      <Copilot />
      <Toast />
    </div>
  );
}
