from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any

from therados.db.session import get_db
from therados.models.domain_models import EvidenceClaim, BiologicalEntity
from scientific.graphs.triclique_engine import TricliqueEngine

router = APIRouter(prefix="/graphs", tags=["Multipartite & Causal Graph"])
triclique_engine = TricliqueEngine()

@router.get("")
async def get_multipartite_graph(db: AsyncSession = Depends(get_db)):
    # Build graph nodes and edges from database
    entities_res = await db.execute(select(BiologicalEntity))
    entities = entities_res.scalars().all()

    claims_res = await db.execute(select(EvidenceClaim))
    claims = claims_res.scalars().all()

    nodes = [
        {"data": {"id": e.id, "label": e.name, "type": e.entity_type, "symbol": e.canonical_symbol or e.name}}
        for e in entities
    ]

    edges = [
        {"data": {"id": c.id, "source": c.subject_entity_id, "target": c.object_entity_id, "label": c.predicate, "maturity": c.evidence_maturity}}
        for c in claims
    ]

    return {"nodes": nodes, "edges": edges}

@router.post("/triclique")
async def run_triclique_inference():
    # Run exact triclique candidate inference
    drugs = ["RP-6306", "Dinaciclib", "Adavosertib"]
    targets = ["PKMYT1", "CDK2", "WEE1"]
    diseases = ["Platinum-Resistant HGSOC", "CCNE1-Amp Ovarian"]

    dt_edges = [("RP-6306", "PKMYT1"), ("Dinaciclib", "CDK2")]
    td_edges = [("PKMYT1", "Platinum-Resistant HGSOC"), ("CDK2", "Platinum-Resistant HGSOC")]
    dd_edges = [("RP-6306", "Platinum-Resistant HGSOC")]

    candidates = triclique_engine.find_candidate_edges(drugs, targets, diseases, dt_edges, td_edges, dd_edges)
    return {"candidates": candidates}
