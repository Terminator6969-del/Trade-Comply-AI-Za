# TradeComply AI South Africa MVP

**AI-Powered Trade Compliance Automation for South Africa**

A B2B SaaS platform enabling clearing agents, freight forwarders, and importers/exporters to validate shipment compliance before SARS submission, with deterministic rule engine + AI-powered extraction and classification.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Node.js 18+
- PostgreSQL 16 (or use docker-compose)

### Setup (5 minutes)

```bash
# 1. Clone & install dependencies
make install

# 2. Start all services (PostgreSQL, Redis, MinIO, API, Worker, Web)
make up

# 3. Run migrations
make migrate

# 4. Seed database with sample tariffs & rules
make seed

# 5. Access the app
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/api/v1/docs
```

### Demo Credentials

**Admin User:**
- Email: `admin@demo.com`
- Password: `demo-password-123`
- Organization: TradeComply Demo

**Sample Shipment:** Pre-created on first seed

## Architecture

### Monorepo Structure

```
tradecomply-ai-za/
├── apps/
│   ├── api/                 # FastAPI backend (Python 3.12)
│   │   ├── app/
│   │   │   ├── core/        # Config, DB, security, dependencies
│   │   │   ├── models/      # SQLAlchemy ORM models
│   │   │   ├── schemas/     # Pydantic request/response schemas
│   │   │   ├── routers/     # API route handlers
│   │   │   ├── services/    # Business logic layer
│   │   │   ├── ai/          # LLM & OCR provider abstractions
│   │   │   ├── rules/       # Compliance rule engine
│   │   │   ├── workers/     # Celery background tasks
│   │   │   └── main.py      # FastAPI app entry point
│   │   ├── tests/           # Pytest unit & integration tests
│   │   ├── alembic/         # Database migrations
│   │   ├── pyproject.toml   # Python dependencies & config
│   │   └── Dockerfile       # API service image
│   │
│   ├── web/                 # Next.js 14 frontend (TypeScript)
│   │   ├── app/             # App Router pages & layouts
│   │   ├── components/      # React components
│   │   ├── lib/             # API hooks, utilities, auth
│   │   ├── public/          # Static assets
│   │   ├── package.json     # Node dependencies
│   │   ├── tsconfig.json    # TypeScript config
│   │   ├── tailwind.config.js
│   │   └── Dockerfile       # Frontend service image
│   │
│   └── api.worker/          # Celery worker (separate service)
│       └── Dockerfile       # Worker service image
│
├── packages/
│   └── shared-types/        # TypeScript type definitions (codegen)
│       └── src/
│
├── infra/
│   ├── docker-compose.yml   # Local dev stack (6 services)
│   ├── .env.example         # Environment template
│   └── nginx.conf           # Reverse proxy (optional)
│
├── scripts/
│   ├── seed.py              # Database seeding (tariffs, rules, demo data)
│   └── migrate.sh           # Migration helpers
│
├── Makefile                 # Build & deployment commands
├── README.md                # This file
├── .gitignore               # Git ignore patterns
└── Claude.MD                # Development rules & constraints
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form |
| **Backend** | FastAPI, Python 3.12, Pydantic v2, SQLAlchemy 2.0 |
| **Database** | PostgreSQL 16, pgvector (embeddings) |
| **Cache/Queue** | Redis, Celery (background jobs) |
| **File Storage** | MinIO (S3-compatible) |
| **Authentication** | JWT, Argon2 password hashing |
| **Testing** | pytest, Playwright E2E |
| **Deployment** | Docker Compose (local), Kubernetes (prod) |

## Core Features

### Phase 1: Document Ingestion & Extraction
- PDF/image upload with virus scanning
- Mock OCR → field extraction (invoice #, HS codes, values)
- Celery workers for async processing
- Confidence scoring on all extractions

### Phase 2: HS Code Classification
- Vector embeddings for tariff search
- LLM-powered ranking (top-5 HS codes with reasoning)
- South African tariff database (8000+ codes)
- Duty & VAT lookup

### Phase 3: Compliance Validation
- Deterministic rule engine (SARS, ITAC, NRCS, Dangerous Goods, Valuation)
- Risk scoring (low/medium/high)
- Permit requirement flags
- No autonomous SARS submission (human review always required)

### Phase 4: Customs Packet Generation
- JSON, CSV, PDF export formats
- Complete shipment summary with recommendations
- Audit trail of all calculations

### Phase 5: Multi-Tenant SaaS
- RBAC (Owner, Admin, Compliance Manager, Clerk, Viewer, API Service)
- Organization isolation (every query filters by org_id)
- Usage tracking & analytics
- API key management

## API Routes

### Authentication
- `POST /api/v1/auth/register` - Register new user + organization
- `POST /api/v1/auth/login` - Login & receive JWT tokens
- `POST /api/v1/auth/refresh` - Refresh expired token

### Organizations
- `GET /api/v1/organizations/me` - Get current organization
- `POST /api/v1/organizations` - Create organization
- `GET /api/v1/organizations/{id}` - Get org details

### Shipments
- `POST /api/v1/shipments` - Create shipment
- `GET /api/v1/shipments` - List shipments (filtered by org)
- `GET /api/v1/shipments/{id}` - Shipment detail
- `PATCH /api/v1/shipments/{id}` - Update shipment

### Documents
- `POST /api/v1/shipments/{id}/documents` - Upload document
- `GET /api/v1/shipments/{id}/documents` - List documents
- `GET /api/v1/documents/{id}/extraction` - Get extracted fields

### Classification
- `POST /api/v1/shipments/{id}/classify` - Classify line items
- `GET /api/v1/tariffs/search?q=solar&limit=10` - Search tariffs

### Compliance
- `POST /api/v1/shipments/{id}/compliance/check` - Run compliance rules
- `GET /api/v1/shipments/{id}/compliance` - Get compliance report

### Duties
- `POST /api/v1/shipments/{id}/duties/estimate` - Calculate duty & VAT

### Packets
- `POST /api/v1/shipments/{id}/packets?format=json` - Generate export packet

## Development

### Running Tests

```bash
# All tests
make test

# API tests only
make test-api

# With coverage report
make test-api  # generates htmlcov/index.html

# Watch mode
cd apps/api && pytest tests/ -v --tb=short -x
```

### Code Quality

```bash
# Format code
make format

# Lint
make lint

# Type checking
cd apps/api && mypy app/
cd apps/web && npm run type-check
```

### Database Migrations

```bash
# Create new migration
cd apps/api && alembic revision --autogenerate -m "Add new column"

# Apply migrations
make migrate

# Rollback one revision
cd apps/api && alembic downgrade -1
```

## Key Constraints (Claude.MD)

- ✅ Every API route must validate input (Pydantic)
- ✅ Every database query must filter by organization_id
- ✅ No plain-text passwords (Argon2)
- ✅ Audit logs for all mutations
- ✅ AI outputs include confidence scores
- ✅ Compliance checks are deterministic
- ✅ No direct SARS submission
- ✅ All code is fully typed (TypeScript/Python)
- ✅ Add tests for critical paths
- ✅ Keep code modular

## Compliance & Security

### POPIA (South African Data Protection)
- Minimize personal data collection
- Explicit customer consent for model training
- Data deletion on request
- Audit logging of all access

### Customs Compliance
- No autonomous SARS submission (legal liability)
- All AI recommendations include confidence + disclaimer
- Deterministic rule engine for regulatory checks
- Manual approval gates for high-risk shipments

### Security
- JWT authentication with HS256
- Argon2 password hashing
- API rate limiting (coming)
- TLS/HTTPS (prod)
- SQL injection prevention (parameterized queries)
- Secrets management (env vars, never committed)

## Deployment

### Local Development
```bash
make up      # Starts all 6 services
make down    # Stops all services
```

### Production (Recommended: Kubernetes)
- See `infra/k8s/` for manifests
- Environment: Set all vars in secrets manager
- Database: Managed PostgreSQL (AWS RDS, Azure, GCP Cloud SQL)
- Storage: S3, Azure Blob Storage, or GCS
- Queue: Managed Redis (AWS ElastiCache, Azure Cache, GCP Memorystore)

## Troubleshooting

### Port conflicts
```bash
# Check what's using port 5432 (postgres)
lsof -i :5432
# Change in .env and docker-compose.yml
```

### Database won't start
```bash
# Remove volume and recreate
docker-compose -f infra/docker-compose.yml down -v
make up
make migrate
make seed
```

### Worker not processing jobs
```bash
# Check Redis connection
docker exec tradecomply-redis redis-cli ping  # Should return PONG
# Check Celery logs
docker-compose logs api-worker
```

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Write tests first (TDD)
3. Implement code
4. Run tests: `make test`
5. Format: `make format`
6. Commit with atomic message
7. Push & create PR

## License

Proprietary © 2026 TradeComply AI South Africa. All rights reserved.

## Support

- **Documentation:** See `docs/` folder
- **Issues:** GitHub Issues
- **Email:** support@tradecomply.ai
- **Status:** https://status.tradecomply.ai

---

**Built with ❤️ for South African trade compliance automation**
