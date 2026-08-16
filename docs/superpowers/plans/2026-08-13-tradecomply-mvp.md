# TradeComply AI South Africa MVP Implementation Plan

**Date:** 2026-08-13  
**Scope:** Complete MVP with monorepo, multi-tenant SaaS, extraction, classification, compliance, packet generation  
**Timeline:** 6 phases, 20 core tasks  
**Tech Stack:** Next.js 14 | FastAPI | SQLAlchemy 2.0 | PostgreSQL + pgvector | Celery + Redis | MinIO | Mock AI

---

## Phase 0: Foundation (Tasks 001-005)

### Task 001: Initialize Monorepo Structure
**Goal:** Set up repo skeleton, Docker Compose, CI/CD  
**Test-First:** `test_monorepo_structure()` verifies apps/, infra/, Makefile exist

### Task 002: Database Setup with SQLAlchemy 2.0
**Goal:** Async PostgreSQL engine, models for orgs/users/memberships  
**Test-First:** `test_database_connection()`, `test_models_registered()`

### Task 003: Authentication & Authorization
**Goal:** JWT tokens, Argon2 hashing, role-based access control  
**Test-First:** `test_password_hashing()`, `test_register_and_login()`

### Task 004: Organization & RBAC
**Goal:** Org CRUD, multi-tenancy isolation, role permissions  
**Test-First:** `test_create_organization()`, `test_get_current_org()`

### Task 005: Main App Entry Point
**Goal:** FastAPI app with all routers registered, health check  
**Test-First:** `test_app_exists()`, `test_openapi_schema()`

---

## Phase 1: Core Domain (Tasks 006-007)

### Task 006: Party Management
**Goal:** Import/exporter/supplier/consignee/clearing agent CRUD  
**Test-First:** `test_create_party()`

### Task 007: Shipment Management
**Goal:** Create/list/get shipments with status and risk tracking  
**Test-First:** `test_create_shipment()` verifies status defaults to draft, risk_level to low

---

## Phase 2: Extraction (Tasks 008-010)

### Task 008: Document Upload & Storage
**Goal:** Upload PDFs/images, validate file types, trigger extraction job  
**Test-First:** `test_upload_document()`

### Task 009: Mock OCR & LLM Providers
**Goal:** Provider abstraction, mock implementations for text/field extraction  
**Test-First:** `test_mock_ocr_extracts_text()`, `test_extract_fields_returns_confidence()`

### Task 010: Extraction Worker (Celery)
**Goal:** Background job to OCR → LLM extraction → store fields/line items  
**Test-First:** `test_process_document_updates_status()`

---

## Phase 3: Classification (Tasks 011-012)

### Task 011: Tariff Records & Seed Data
**Goal:** South African tariff DB (8541, 8504, 8507, etc.), compliance rules  
**Test-First:** `test_tariff_record_model()`, `test_seed_tariff_data()`

### Task 012: Classification Pipeline
**Goal:** Vector search + LLM ranking for top-5 HS codes  
**Test-First:** `test_classify_solar_panel()` expects 8541.40 match with 0.85+ confidence

---

## Phase 4: Compliance (Tasks 013)

### Task 013: Compliance Rule Engine
**Goal:** Deterministic rules (SARS/ITAC/NRCS/DG), risk scoring  
**Test-First:** `test_missing_invoice_detected()`, `test_dangerous_goods_flagged()`

---

## Phase 5: Packet & UI (Tasks 014-018)

### Task 014: Duty Estimation
**Goal:** Calculate VAT (15%), customs duty, total with assumptions + disclaimer  
**Test-First:** `test_duty_calculation()`

### Task 015: Packet Generation
**Goal:** JSON/CSV/PDF packets with all shipment data  
**Test-First:** `test_generate_json_packet()`

### Task 016: Frontend Setup
**Goal:** Next.js 14, auth, API hooks, layout  
**Test-First:** `test_homepage_loads()`, `test_can_navigate_to_login()`

### Task 017: Frontend Shipment Management
**Goal:** Dashboard, shipment list, form  
**Test-First:** `test_can_create_shipment()`

### Task 018: Frontend Shipment Detail & Review
**Goal:** Detail page with document/extraction/classification/compliance tabs  
**Test-First:** `test_can_upload_document_and_view_extraction()`

---

## Phase 6: Hardening (Tasks 019-020)

### Task 019: Docker Compose & Integration
**Goal:** Runnable docker-compose.yml, Makefile, README  
**Test-First:** `docker-compose up` starts all services

### Task 020: Final Integration Tests
**Goal:** End-to-end test: register → create shipment → upload → extract → classify → comply → packet  
**Test-First:** `test_full_import_flow()` exercises all APIs

---

## Execution Paths

**Option A: Subagent-Driven (Recommended)**  
Launch Explore subagent per task phase, review outputs, iterate fast

**Option B: Inline Sequential**  
Execute all tasks in this session with checkpoint reviews

**Which approach do you prefer?**

---

## Key Success Criteria

✅ Docker Compose runs all services  
✅ All routes validate input (Pydantic/Zod)  
✅ All DB queries filter by organization_id  
✅ JWT auth with Argon2 hashing  
✅ Mock OCR/LLM providers (no external keys required)  
✅ Extraction with confidence scores  
✅ Classification top-5 with reasoning  
✅ Compliance checks with severity  
✅ Duty estimate with disclaimer  
✅ Audit logs for all mutations  
✅ Frontend dashboard + shipment list + detail tabs  
✅ Tests for critical paths  

---

**Ready to proceed with implementation?**
