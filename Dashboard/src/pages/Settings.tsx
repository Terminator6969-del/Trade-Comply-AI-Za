import { useState } from "react";
import { team } from "../lib/data";
import { workspaces } from "../lib/data";
import { Card } from "../components/ui";
import { useApp } from "../lib/store";
import { clsx } from "../lib/format";
import { Copy, Plus, Trash2 } from "lucide-react";

const tabs = ["Organisation", "Users", "API keys", "Billing"] as const;

export function Settings() {
  const { dark, toggleDark, workspace, setWorkspace, setToast } = useApp();
  const [tab, setTab] = useState<(typeof tabs)[number]>("Organisation");
  const [keys, setKeys] = useState([
    { id: "k1", name: "Cape Town production", hint: "tc_live_8f2a…91c", created: "12 Mar 2026" },
    { id: "k2", name: "Sandbox EDI", hint: "tc_test_11ab…e04", created: "02 Feb 2026" },
  ]);
  return (
    <div className="space-y-5">
      <div>
        <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-[#8a968e]">Workspace</p>
        <h1 className="mt-1 text-[28px] font-semibold tracking-tight">Settings</h1>
      </div>
      <div className="flex gap-1 overflow-x-auto rounded-full bg-white/70 p-1 ring-1 ring-[#e6eae2] dark:bg-white/5 dark:ring-white/8">
        {tabs.map((t) => (
          <button key={t} onClick={() => setTab(t)} className={clsx("rounded-full px-4 py-1.5 text-[13px] font-semibold", tab === t ? "bg-[#0F2B24] text-white dark:bg-[#A3E635] dark:text-[#0F2B24]" : "text-[#5c6b64]")}>
            {t}
          </button>
        ))}
      </div>

      {tab === "Organisation" && <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
        <Card>
          <h3 className="text-[15px] font-semibold">Appearance</h3>
          <p className="mt-1 text-[13px] text-[#6b7a72]">Match the Cape Town control room or a late Durban shift.</p>
          <button
            onClick={toggleDark}
            className="mt-4 h-10 rounded-full bg-[#0F2B24] px-4 text-[13px] font-semibold text-white dark:bg-[#A3E635] dark:text-[#0F2B24]"
          >
            Switch to {dark ? "light" : "dark"} mode
          </button>
        </Card>
        <Card>
          <h3 className="text-[15px] font-semibold">Default hub</h3>
          <p className="mt-1 text-[13px] text-[#6b7a72]">Used for landing filters and SARS office codes.</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {workspaces.map((w) => (
              <button
                key={w.id}
                onClick={() => setWorkspace(w.id)}
                className={`rounded-full px-3 py-1.5 text-[12px] font-semibold ${
                  workspace === w.id
                    ? "bg-[#0F2B24] text-white dark:bg-[#A3E635] dark:text-[#0F2B24]"
                    : "bg-[#eef1ea] text-[#0F2B24] dark:bg-white/8 dark:text-white"
                }`}
              >
                {w.name}
              </button>
            ))}
          </div>
        </Card>
        <Card className="lg:col-span-2">
          <h3 className="text-[15px] font-semibold">Organisation</h3>
          <dl className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3 text-[13px]">
            <div><dt className="text-[#8a968e]">Legal name</dt><dd className="mt-0.5 font-semibold">TradeComply AI (Pty) Ltd</dd></div>
            <div><dt className="text-[#8a968e]">VAT</dt><dd className="mt-0.5 font-semibold">4210 882 114</dd></div>
            <div><dt className="text-[#8a968e]">SARS client</dt><dd className="mt-0.5 font-semibold">AEO-ZA-44102</dd></div>
          </dl>
        </Card>
      </div>}

      {tab === "Users" && <Card>
          <h3 className="text-[15px] font-semibold">Team</h3>
          <ul className="mt-4 divide-y divide-[#eef1ea] dark:divide-white/8">
            {team.map((m) => (
              <li key={m.email} className="flex items-center gap-3 py-3">
                <img src={m.img} alt="" className="h-10 w-10 rounded-full object-cover" />
                <div className="min-w-0 flex-1">
                  <p className="text-[13.5px] font-semibold">{m.name}</p>
                  <p className="text-[12px] text-[#6b7a72]">
                    {m.role} · {m.email}
                  </p>
                </div>
                <span className="rounded-full bg-[#eef1ea] px-2 py-0.5 text-[11px] font-semibold dark:bg-white/8">
                  Active
                </span>
              </li>
            ))}
          </ul>
        </Card>}

      {tab === "API keys" && (
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-[15px] font-semibold">API keys</h3>
              <p className="text-[12px] text-[#6b7a72]">Scoped to /api/v1 · rotate from the Cape Town hub.</p>
            </div>
            <button
              onClick={() => {
                setKeys((k) => [{ id: `k${Date.now()}`, name: "New key", hint: "tc_live_••••", created: "Just now" }, ...k]);
                setToast("API key minted.");
                window.setTimeout(() => setToast(null), 2000);
              }}
              className="inline-flex h-9 items-center gap-1 rounded-full bg-[#0F2B24] px-3 text-[12px] font-semibold text-white dark:bg-[#A3E635] dark:text-[#0F2B24]"
            >
              <Plus className="h-3.5 w-3.5" /> Mint key
            </button>
          </div>
          <ul className="mt-4 divide-y divide-[#eef1ea] dark:divide-white/8">
            {keys.map((k) => (
              <li key={k.id} className="flex items-center gap-3 py-3">
                <div className="flex-1">
                  <p className="text-[13px] font-semibold">{k.name}</p>
                  <p className="font-mono text-[12px] text-[#6b7a72]">{k.hint} · {k.created}</p>
                </div>
                <button onClick={() => { navigator.clipboard?.writeText(k.hint); setToast("Copied."); window.setTimeout(() => setToast(null), 1600); }} className="rounded-full p-2 hover:bg-[#eef1ea] dark:hover:bg-white/8"><Copy className="h-4 w-4" /></button>
                <button onClick={() => setKeys((list) => list.filter((x) => x.id !== k.id))} className="rounded-full p-2 hover:bg-rose-50"><Trash2 className="h-4 w-4 text-rose-600" /></button>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {tab === "Billing" && (
        <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
          <Card>
            <p className="text-[12px] text-[#8a968e]">Plan</p>
            <p className="mt-1 text-[22px] font-semibold">Control tower</p>
            <p className="mt-1 text-[13px] text-[#6b7a72]">R 48 000 / month · 5 seats · unlimited EDI</p>
            <button className="mt-4 h-10 rounded-full bg-[#0F2B24] px-4 text-[13px] font-semibold text-white dark:bg-[#A3E635] dark:text-[#0F2B24]">Manage billing</button>
          </Card>
          <Card>
            <h3 className="text-[15px] font-semibold">Usage this cycle</h3>
            <ul className="mt-3 space-y-2 text-[13px]">
              <li className="flex justify-between"><span className="text-[#6b7a72]">Shipments scored</span><span className="tabular font-semibold">186</span></li>
              <li className="flex justify-between"><span className="text-[#6b7a72]">Documents extracted</span><span className="tabular font-semibold">412</span></li>
              <li className="flex justify-between"><span className="text-[#6b7a72]">Copilot tokens</span><span className="tabular font-semibold">2.1m</span></li>
            </ul>
          </Card>
        </div>
      )}

      {tab === "Organisation" && <Card>
          <h3 className="text-[15px] font-semibold">Integrations</h3>
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
            {[
              { name: "SARS eFiling / EDI", state: "Connected" },
              { name: "ITAC permits", state: "Connected" },
              { name: "Transnet Navis", state: "Sandbox" },
            ].map((i) => (
              <div key={i.name} className="rounded-xl border border-[#eef1ea] p-3 dark:border-white/8">
                <p className="text-[13px] font-semibold">{i.name}</p>
                <p className="mt-1 text-[12px] text-emerald-700 dark:text-emerald-300">{i.state}</p>
              </div>
            ))}
          </div>
        </Card>}
    </div>
  );
}
