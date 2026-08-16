# TradeComply AI South Africa — Dashboard Build Specification

## Context
**Project**: TradeComply AI South Africa — B2B SaaS for trade compliance automation  
**Stack**: Next.js 14 (App Router), TypeScript, Tailwind CSS, React Query, Zustand  
**Current State**: Only `/dashboard` page exists with static KPI cards and a mock `ShipmentList` component  
**Backend API**: FastAPI at `http://localhost:8000/api/v1` with OpenAPI docs at `/api/v1/docs`

---

## Pages to Build

| Route | Purpose | Key Components |
|-------|---------|----------------|
| `/dashboard` | Overview with KPIs, recent shipments, AI insights | KPICard, ShipmentList, AIInsightsWidget |
| `/shipments` | List/filter/create shipments | ShipmentTable, ShipmentFilters, CreateShipmentModal |
| `/shipments/[id]` | Shipment detail with compliance, documents, line items | ShipmentHeader, CompliancePanel, DocumentList, LineItemTable |
| `/documents` | Document upload, extraction status, review | DocumentTable, UploadZone, ExtractionReviewPanel |
| `/compliance` | Compliance reports, rule violations, risk trends | ComplianceReportList, RuleViolationTable, RiskTrendChart |
| `/parties` | Importers, suppliers, clearing agents CRUD | PartyTable, PartyFormModal |
| `/tariffs` | HS code search, duty calculator | TariffSearch, DutyCalculator |
| `/settings` | Org settings, users, API keys, billing | SettingsTabs, UserManagement, APIKeyManager |

---

## API Endpoints Available (from OpenAPI)

```typescript
// Shipments
GET    /api/v1/shipments                    // List with pagination, filters
POST   /api/v1/shipments                    // Create
GET    /api/v1/shipments/{id}               // Detail with relations
PATCH  /api/v1/shipments/{id}               // Update
DELETE /api/v1/shipments/{id}               // Delete
POST   /api/v1/shipments/{id}/compliance    // Run compliance check

// Documents
POST   /api/v1/documents/upload             // Multipart upload
GET    /api/v1/shipments/{id}/documents     // List for shipment
GET    /api/v1/documents/{id}               // Detail + extraction
PATCH  /api/v1/documents/{id}/extract       // Trigger extraction

// Compliance
GET    /api/v1/compliance/shipments/{id}    // Full compliance report
GET    /api/v1/compliance/rules             // List all rules

// Parties
GET    /api/v1/parties                      // List with type filter
POST   /api/v1/parties                      // Create
PATCH  /api/v1/parties/{id}                 // Update

// Tariffs
GET    /api/v1/tariffs/search?q=...         // HS code search
POST   /api/v1/tariffs/calculate-duty       // Duty calculation

// Auth/Org
GET    /api/v1/organizations/me             // Current org
GET    /api/v1/auth/me                      // Current user
```

---

## Design System (Already Configured)

```typescript
// tailwind.config.js colors
colors: {
  primary: { 500: '#A3E635', 600: '#84CC16' },  // Lime green brand
  surface: '#FFFFFF',
  background: '#F4F5F7',
  text: { primary: '#111827', secondary: '#6B7280' },
  border: '#E5E7EB',
  status: {
    success: '#10B981',
    warning: '#F59E0B',
    error: '#EF4444',
    info: '#3B82F6',
  }
}

// Components use: rounded-2xl, shadow-sm, transition-all duration-200
// Icons: @heroicons/react/24/outline + solid variants
```

---

## Component Architecture Needed

```
components/
├── ui/                    # Base primitives
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Select.tsx
│   ├── Modal.tsx
│   ├── Table.tsx
│   ├── Badge.tsx
│   ├── Card.tsx
│   └── Dropdown.tsx
├── dashboard/             # Dashboard-specific
│   ├── KPICard.tsx        ✅ exists
│   ├── ShipmentList.tsx   ✅ exists (needs real data)
│   └── AIInsightsWidget.tsx
├── shipments/
│   ├── ShipmentTable.tsx
│   ├── ShipmentFilters.tsx
│   ├── CreateShipmentModal.tsx
│   ├── ShipmentDetailHeader.tsx
│   ├── CompliancePanel.tsx
│   ├── DocumentList.tsx
│   └── LineItemTable.tsx
├── documents/
│   ├── DocumentTable.tsx
│   ├── UploadZone.tsx
│   └── ExtractionReviewPanel.tsx
├── compliance/
│   ├── ComplianceReportCard.tsx
│   ├── RuleViolationRow.tsx
│   └── RiskTrendChart.tsx  (use recharts)
└── layout/
    ├── Sidebar.tsx        ✅ exists
    └── Header.tsx         ✅ exists
```

---

## Auth Integration

```typescript
// lib/auth.ts - Already has:
- useAuth() hook with user, org, tokens
- axios instance with auto-refresh
- Protected route wrapper

// Usage:
const { user, organization, isLoading } = useAuth();
const { data: shipments } = useShipments({ page: 1, status: 'draft' });
```

---

## State Management (Zustand)

```typescript
// stores/shipmentStore.ts
interface ShipmentState {
  filters: ShipmentFilters;
  setFilters: (f: Partial<ShipmentFilters>) => void;
  selectedShipment: Shipment | null;
  setSelectedShipment: (s: Shipment | null) => void;
}
```

---

## Acceptance Criteria per Page

### `/shipments`
- [ ] Server-side pagination (10/25/50)
- [ ] Filters: status, risk_level, date range, search by reference
- [ ] Column sorting (reference, created_at, risk_level)
- [ ] Row click → navigate to `/shipments/[id]`
- [ ] "New Shipment" modal with party selectors (typeahead from `/parties`)

### `/shipments/[id]`
- [ ] Header: reference, status badge, risk badge, incoterms, currency
- [ ] Tabs: Overview | Compliance | Documents | Line Items | Audit Log
- [ ] Compliance tab: run check button, show report with expandable rules
- [ ] Documents tab: upload zone, list with extraction status badges
- [ ] Line Items tab: editable table (hs_code_suggested, confidence)

### `/documents`
- [ ] Drag-drop upload (max 10MB, PDF/JPG/PNG)
- [ ] Show extraction status: pending → processing → completed/failed
- [ ] Click row → side panel with extracted fields + confidence scores
- [ ] "Re-extract" button for failed

### `/compliance`
- [ ] List all compliance reports with risk_level summary
- [ ] Filter by date, risk_level, rule_code
- [ ] Drill-down to shipment detail
- [ ] Chart: compliance rate over time (recharts)

---

## Quick Start Commands

```bash
# 1. Install deps
cd apps/web && npm install

# 2. Run dev server
npm run dev

# 3. View API types (after backend running)
npm run type-check  # or generate from OpenAPI
```

---

## Pro Tips

1. **Generate TypeScript types from OpenAPI**:
   ```bash
   npx openapi-typescript http://localhost:8000/api/v1/openapi.json -o lib/api/schema.ts
   ```

2. **Use React Query for all server state** — caching, invalidation, optimistic updates

3. **Keep components small** — extract `ShipmentRow`, `DocumentRow`, `RuleBadge` etc.

4. **Error boundaries** per page section (compliance panel, document list)

5. **Loading skeletons** for tables/cards (shadcn/ui pattern)

---

## First Sprint Priority

1. **Shipments list** with real data + pagination + filters
2. **Shipment detail** with compliance + documents tabs
3. **Document upload** with extraction status
4. **Compliance report view** (read-only from API)