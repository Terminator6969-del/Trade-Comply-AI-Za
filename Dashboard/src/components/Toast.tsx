import { AnimatePresence, motion } from "framer-motion";
import { Check } from "lucide-react";
import { useApp } from "../lib/store";

export function Toast() {
  const toast = useApp((s) => s.toast);
  return (
    <AnimatePresence>
      {toast && (
        <motion.div
          initial={{ y: 16, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 10, opacity: 0 }}
          className="fixed bottom-6 left-1/2 z-[80] flex -translate-x-1/2 items-center gap-2 rounded-full bg-[#0F2B24] px-4 py-2.5 text-[13px] font-semibold text-white shadow-xl"
        >
          <Check className="h-4 w-4 text-[#A3E635]" />
          {toast}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
