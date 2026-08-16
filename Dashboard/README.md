# TradeComply AI South Africa — SaaS Dashboard

Modern, AI-powered compliance automation dashboard for the South African cross-border trade market.

## Features

- **Overview Dashboard (`/dashboard`)**:
  - Live metric cards (Customs value, duty assessed, compliance rate, risk indicators)
  - Interactive charts (Compliance score trends, risk distribution, trade lanes, AI insights)
  - Quick actions (Export CSV, New shipment wizard)
  - Shipments table with live search and status filters

- **Shipments (`/shipments` & `/shipments/:id`)**:
  - Live book tracking imports and exports (Rotterdam, Durban, Houston, Antwerp, etc.)
  - 5-tab detail view:
    1. **Overview**: Key customs data, SARS MRN references, Incoterms, container count, weight
    2. **Compliance**: Multi-agency rule checks (SARS, ITAC, SAHPRA, NRCS, DALRRD) with legal references
    3. **Documents**: OCR extracted fields with confidence scoring
    4. **Line Items**: Harmonized Tariff code suggestions vs confirmed classification
    5. **Audit Log**: Mutation history, SARS EDI events, user actions
  - **Run Compliance** simulation action with instant report updates

- **Documents Control Center (`/documents`)**:
  - Drag-and-drop document upload (PDF, JPG, PNG up to 10MB)
  - Automated OCR extraction simulation with confidence progress bars
  - Field-level detail drawer (SAD500, commercial invoices, EUR.1 origin certificates)
  - Re-extraction trigger for failed/rejected scans

- **Compliance Control Tower (`/compliance`)**:
  - Real-time governance KPIs (SARS first-pass rate, ITAC permit coverage, AEO status)
  - Filterable compliance reports scored against regulatory rules
  - Exception queue for urgent compliance reviews

- **Trade Parties (`/parties`)**:
  - Directory of Importers, Exporters, Carriers, Brokers, and Consignees
  - VAT / TIN verification, risk ratings, and shipment volume metrics
  - "Add Party" creation modal

- **Tariffs & HS Codes (`/tariffs`)**:
  - SARS Schedule 1 HS code explorer with duty rates, VAT, and ITAC permit flags
  - **Interactive Duty & VAT Calculator**: Estimate payable customs duties and VAT based on CIF ZAR value and net mass

- **Settings (`/settings`)**:
  - **Organisation**: Dark/Light mode appearance toggle, default hub selection (Cape Town / Durban / Johannesburg), legal entity info
  - **Users**: Team roster with roles and avatars
  - **API Keys**: Mint new keys, copy to clipboard, delete keys
  - **Billing & Usage**: Plan overview and usage meters (scored shipments, extracted docs, copilot tokens)
  - **Integrations**: SARS eFiling/EDI, ITAC permits, Transnet Navis status

- **Interactive Global Tools**:
  - **AI Copilot**: Floating drawer with prompt presets for fast classification and SAD500 line drafting
  - **Command Palette (`⌘K` / `Ctrl+K`)**: Instant search across all pages, shipments, and HS tariff codes
  - **New Shipment Modal**: Step-by-step shipment wizard

## Running Locally

```bash
# Install dependencies
npm install

# Start development server (http://localhost:5173)
npm run dev

# Build production bundle
npm run build

# Preview production build
npm run preview
```
