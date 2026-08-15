from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from therados.db.session import get_db
from therados.models.domain_models import TherapeuticProgram, TherapeuticHypothesis, EvidenceClaim
from therados.schemas.domain_schemas import CopilotQueryRequest, CopilotQueryResponse
from integrations.model_providers.copilot_engine import CopilotEngine

router = APIRouter(prefix="/copilot", tags=["AI Copilot Workspace"])
copilot_engine = CopilotEngine()

@router.post("/query", response_model=CopilotQueryResponse)
async def query_copilot(req: CopilotQueryRequest, db: AsyncSession = Depends(get_db)):
    prog_res = await db.execute(select(TherapeuticProgram).where(TherapeuticProgram.id == req.program_id))
    prog = prog_res.scalar_one_or_none()
    disease_name = prog.disease if prog else "Therapeutic Program"

    hypos_res = await db.execute(select(TherapeuticHypothesis).where(TherapeuticHypothesis.program_id == req.program_id))
    hypos = [{"id": h.id, "title": h.title, "status": h.status, "support_score": h.support_score} for h in hypos_res.scalars().all()]

    claims_res = await db.execute(select(EvidenceClaim))
    claims = [{"evidence_record_id": c.evidence_record_id, "subject": c.subject_entity_id, "predicate": c.predicate, "object": c.object_entity_id, "evidence_maturity": c.evidence_maturity} for c in claims_res.scalars().all()]

    res = copilot_engine.query_copilot(req.query, disease_name, hypos, claims)
    return CopilotQueryResponse(
        answer=res["answer"],
        citations=res["citations"],
        confidence=res["confidence"],
        uncertainties=res["uncertainties"]
    )
