.PHONY: help bootstrap infra migrate seed dev test lint typecheck verify clean docker-build generate-client

help:
	@echo "TheraDOS Development Commands:"
	@echo "  make bootstrap       - Install dependencies for backend and frontend"
	@echo "  make infra           - Start local infrastructure (Postgres, Neo4j, Redis, MinIO, Temporal)"
	@echo "  make migrate         - Run database migrations"
	@echo "  make seed            - Seed database with synthetic tutorial dataset"
	@echo "  make dev             - Run development servers (backend & frontend)"
	@echo "  make test            - Run backend and frontend test suites"
	@echo "  make lint            - Run linters for backend and frontend"
	@echo "  make typecheck       - Run typecheckers (mypy & tsc)"
	@echo "  make generate-client - Generate OpenAPI schema JSON specification"
	@echo "  make verify          - Run full verification (lint, typecheck, tests)"
	@echo "  make clean           - Clean build artifacts and caches"

bootstrap:
	cd backend && pip install -e ".[dev]"
	cd apps/web && npm install

infra:
	docker compose up -d postgres neo4j redis minio temporal

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python -m therados.db.seed_tutorial

dev:
	@echo "Starting backend and frontend dev servers..."
	(trap 'kill 0' SIGINT; cd backend && uvicorn therados.main:app --reload --port 8000 & cd apps/web && npm run dev)

test:
	cd backend && pytest
	cd apps/web && npm run test -- --passWithNoTests

lint:
	cd backend && ruff check .
	cd apps/web && npm run lint

typecheck:
	cd backend && mypy therados
	cd apps/web && npm run typecheck

generate-client:
	PYTHONPATH=backend:. python3 -c "import json; from therados.main import app; print(json.dumps(app.openapi(), indent=2))" > docs/openapi.json

verify: lint typecheck test generate-client

docker-build:
	docker compose build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".next" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
