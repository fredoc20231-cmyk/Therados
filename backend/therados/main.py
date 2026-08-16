from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, AsyncGenerator
import logging

from therados.config.settings import settings
from therados.db.session import init_db
from therados.api.health import router as health_router
from therados.api.auth import router as auth_router
from therados.api.projects import router as projects_router
from therados.api.programs import router as programs_router
from therados.api.evidence import router as evidence_router
from therados.api.graphs import router as graphs_router
from therados.api.endotypes import router as endotypes_router
from therados.api.hypotheses import router as hypotheses_router
from therados.api.pharmacology import router as pharmacology_router
from therados.api.candidates import router as candidates_router
from therados.api.portfolio import router as portfolio_router
from therados.api.experiments import router as experiments_router
from therados.api.decisions import router as decisions_router
from therados.api.copilot import router as copilot_router
from therados.api.models import router as models_router
from therados.api.integrations import router as integrations_router
from therados.api.audit import router as audit_router
from therados.api.discovery import router as discovery_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("therados.main")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        await init_db()
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")
    yield

app = FastAPI(
    title="TheraDOS — Therapeutic Domain Operating System",
    description="Provenance-aware therapeutic intelligence operating system converting heterogeneous evidence into falsifiable, safety-constrained hypotheses.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health routes
app.include_router(health_router)

# v1 API routes
v1_prefix = "/api/v1"
app.include_router(auth_router, prefix=v1_prefix)
app.include_router(projects_router, prefix=v1_prefix)
app.include_router(programs_router, prefix=v1_prefix)
app.include_router(evidence_router, prefix=v1_prefix)
app.include_router(graphs_router, prefix=v1_prefix)
app.include_router(endotypes_router, prefix=v1_prefix)
app.include_router(hypotheses_router, prefix=v1_prefix)
app.include_router(pharmacology_router, prefix=v1_prefix)
app.include_router(candidates_router, prefix=v1_prefix)
app.include_router(portfolio_router, prefix=v1_prefix)
app.include_router(experiments_router, prefix=v1_prefix)
app.include_router(decisions_router, prefix=v1_prefix)
app.include_router(copilot_router, prefix=v1_prefix)
app.include_router(models_router, prefix=v1_prefix)
app.include_router(integrations_router, prefix=v1_prefix)
app.include_router(audit_router, prefix=v1_prefix)
app.include_router(discovery_router, prefix=v1_prefix)

@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "message": "Welcome to TheraDOS — Therapeutic Domain Operating System",
        "docs": "/docs",
        "status": "operational"
    }
