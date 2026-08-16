.PHONY: help install up down migrate seed test lint format clean

help:
	@echo "TradeComply AI South Africa - MVP Build Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      - Install all dependencies"
	@echo "  make clean        - Remove all build artifacts"
	@echo ""
	@echo "Development:"
	@echo "  make up           - Start all services (docker-compose)"
	@echo "  make down         - Stop all services"
	@echo "  make logs         - View service logs"
	@echo ""
	@echo "Database:"
	@echo "  make migrate      - Run Alembic migrations"
	@echo "  make seed         - Seed database with sample data"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test         - Run all tests"
	@echo "  make test-api     - Run API tests only"
	@echo "  make test-web     - Run frontend tests only"
	@echo "  make lint         - Run linters (pylint, eslint)"
	@echo "  make format       - Format code (black, prettier)"
	@echo ""

install:
	cd apps/api && pip install -e ".[dev]"
	cd apps/web && npm install
	cd Dashboard && npm install
	cd packages/shared-types && npm install

dashboard:
	cd Dashboard && npm run dev

up:
	docker-compose -f infra/docker-compose.yml up -d

down:
	docker-compose -f infra/docker-compose.yml down

logs:
	docker-compose -f infra/docker-compose.yml logs -f

migrate:
	cd apps/api && alembic upgrade head

seed:
	cd apps/api && python scripts/seed.py

test:
	cd apps/api && pytest tests/ -v
	cd apps/web && npm test -- --passWithNoTests

test-api:
	cd apps/api && pytest tests/ -v --cov=app --cov-report=html

test-web:
	cd apps/web && npm test

lint:
	cd apps/api && pylint app/
	cd apps/web && npm run lint

format:
	cd apps/api && black app/ tests/ && isort app/ tests/
	cd apps/web && npm run format

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	cd apps/api && rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
	cd apps/web && rm -rf .next node_modules .turbo
	cd packages/shared-types && rm -rf dist node_modules
