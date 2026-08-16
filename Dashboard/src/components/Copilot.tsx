import { AnimatePresence, motion } from "framer-motion";
import { ArrowUp, Sparkles, X } from "lucide-react";
import { FormEvent, useState } from "react";
import { useApp } from "../lib/store";

type Msg = { role: "ai" | "user"; text: string };

const seed: Msg[] = [
  {
    role: "ai",
    text: "I can classify HS codes, draft SAD500 lines, and flag ITAC or SAHPRA gaps. Try a product description.",
  },
];

const replies: Record<string, string> = {
  default:
    "Suggested heading 6109.10 — T-shirts, knitted, of cotton. Duty 45% + R3.90/kg, reducible to 0% under EU-SADC EPA with a valid EUR.1. VAT 15%. No ITAC permit.",
  methanol:
    "Heading 2905.11 — Methanol. Duty free. ITAC dual-use check required. IMDG class 3. Export permit ITAC chemicals before SARS stop.",
  wine:
    "Heading 2204.21 — Wine of fresh grapes ≤ 2L. Excise applies on export bond release. SACUM-UK EPA origin available for Felixstowe.",
  loader:
    "Heading 8429.51 — Front-end shovel loaders. Duty 10%. NRCS LOA on safety components and rebate 470.03 if qualifying.",
};

function replyFor(q: string) {
  const s = q.toLowerCase();
  if (s.includes("methanol") || s.includes("chemical")) return replies.methanol;
  if (s.includes("wine") || s.includes("stellenbosch")) return replies.wine;
  if (s.includes("loader") || s.includes("caterpillar") || s.includes("plant")) return replies.loader;
  return replies.default;
}

export function Copilot() {
  const { copilotOpen, setCopilotOpen } = useApp();
  const [msgs, setMsgs] = useState(seed);
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);

  const send = (e?: FormEvent, preset?: string) => {
    e?.preventDefault();
    const q = (preset ?? text).trim();
    if (!q) return;
    setText("");
    setMsgs((m) => [...m, { role: "user", text: q }]);
    setBusy(true);
    window.setTimeout(() => {
      setMsgs((m) => [...m, { role: "ai", text: replyFor(q) }]);
      setBusy(false);
    }, 700);
  };

  return (
    <AnimatePresence>
      {copilotOpen && (
        <>
          <motion.button
            aria-label="Close copilot"
            className="fixed inset-0 z-[60] bg-[#0F2B24]/25 backdrop-blur-[2px]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setCopilotOpen(false)}
          />
          <motion.aside
            initial={{ x: 28, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 24, opacity: 0 }}
            transition={{ type: "spring", stiffness: 340, damping: 32 }}
            className="fixed bottom-3 right-3 top-3 z-[61] flex w-[min(420px,calc(100vw-24px))] flex-col overflow-hidden rounded-[28px] border border-white/50 bg-[#f6f7f2]/92 shadow-[0_24px_80px_rgba(15,43,36,0.22)] backdrop-blur-2xl dark:border-white/10 dark:bg-[#0e221c]/92"
          >
            <div className="relative overflow-hidden px-5 pb-4 pt-5">
              <img src="/images/promo-waves.png" alt="" className="absolute inset-0 h-full w-full object-cover opacity-40" />
              <div className="absolute inset-0 bg-gradient-to-b from-[#0F2B24]/80 to-[#0F2B24]" />
              <div className="relative flex items-start justify-between text-white">
                <div>
                  <div className="inline-flex items-center gap-1 rounded-full bg-[#A3E635]/15 px-2 py-0.5 text-[10px] font-semibold text-[#B7EE55]">
                    <Sparkles className="h-3 w-3" />
                    Copilot
                  </div>
                  <p className="mt-2 text-[17px] font-semibold">Classify & clear faster</p>
                  <p className="mt-0.5 text-[12px] text-white/65">Trained on SARS Schedule 1 and ITAC notices.</p>
                </div>
                <button
                  onClick={() => setCopilotOpen(false)}
                  className="rounded-full p-1.5 text-white/80 hover:bg-white/10"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            </div>

            <div className="flex-1 space-y-3 overflow-y-auto px-4 py-4">
              {msgs.map((m, i) => (
                <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[92%] rounded-2xl px-3.5 py-2.5 text-[13px] leading-relaxed ${
                      m.role === "user"
                        ? "bg-[#0F2B24] text-white"
                        : "bg-white text-[#1d2c26] shadow-sm ring-1 ring-[#e6eae2] dark:bg-white/8 dark:text-[#eef3ea] dark:ring-white/8"
                    }`}
                  >
                    {m.text}
                  </div>
                </div>
              ))}
              {busy && (
                <div className="flex gap-1 px-2">
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[#A3E635]" />
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[#A3E635] [animation-delay:120ms]" />
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[#A3E635] [animation-delay:240ms]" />
                </div>
              )}
            </div>

            <div className="px-4 pb-2">
              <div className="flex flex-wrap gap-1.5">
                {["Cotton tees from Rotterdam", "Methanol export to Houston", "Wine to Felixstowe"].map((p) => (
                  <button
                    key={p}
                    onClick={() => send(undefined, p)}
                    className="rounded-full bg-white px-2.5 py-1 text-[11px] font-medium text-[#3d4d46] ring-1 ring-[#e2e7de] hover:bg-[#f4f6f0] dark:bg-white/5 dark:text-[#d5ddd6] dark:ring-white/10"
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            <form onSubmit={send} className="flex items-center gap-2 px-4 pb-4 pt-2">
              <input
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Describe the goods…"
                className="h-11 flex-1 rounded-full border border-[#e2e7de] bg-white px-4 text-[13px] outline-none ring-[#A3E635]/40 focus:ring-2 dark:border-white/10 dark:bg-white/5 dark:text-white"
              />
              <button
                type="submit"
                className="flex h-11 w-11 items-center justify-center rounded-full bg-[#A3E635] text-[#0F2B24]"
              >
                <ArrowUp className="h-4 w-4" />
              </button>
            </form>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
