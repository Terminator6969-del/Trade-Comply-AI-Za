import { useEffect } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Layout } from "./components/Layout";
import { Overview } from "./pages/Overview";
import { Shipments } from "./pages/Shipments";
import { ShipmentDetail } from "./pages/ShipmentDetail";
import { Documents } from "./pages/Documents";
import { Compliance } from "./pages/Compliance";
import { Parties } from "./pages/Parties";
import { Tariffs } from "./pages/Tariffs";
import { Settings } from "./pages/Settings";
import { initTheme } from "./lib/store";

const queryClient = new QueryClient();

export default function App() {
  useEffect(() => {
    initTheme();
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Overview />} />
            <Route path="shipments" element={<Shipments />} />
            <Route path="shipments/:id" element={<ShipmentDetail />} />
            <Route path="documents" element={<Documents />} />
            <Route path="compliance" element={<Compliance />} />
            <Route path="parties" element={<Parties />} />
            <Route path="tariffs" element={<Tariffs />} />
            <Route path="settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
