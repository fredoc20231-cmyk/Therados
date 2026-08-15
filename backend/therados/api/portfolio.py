from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from therados.db.session import get_db
from therados.models.domain_models import CandidateIntervention, SafetyAssessment
from scientific.portfolio.pareto_engine import ParetoPortfolioEngine

router = APIRouter(prefix="/portfolio", tags=["Pareto Portfolio Engine"])
pareto_engine = ParetoPortfolioEngine()

@router.get("/pareto-ranking")
async def get_pareto_ranking(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(CandidateIntervention))
    candidates = res.scalars().all()

    cand_data = []
    for c in candidates:
        safety_res = await db.execute(select(SafetyAssessment).where(SafetyAssessment.candidate_id == c.id))
        safety = safety_res.scalar_one_or_none()

        cand_data.append({
            "id": c.id,
            "name": c.name,
            "primary_target": c.primary_target,
            "cpi_score": c.cpi_score,
            "novelty_score": c.novelty_score,
            "overall_status": c.overall_status,
            "safety_gate_passed": safety.safety_gate_passed if safety else True
        })

    return pareto_engine.rank_candidates(cand_data)
