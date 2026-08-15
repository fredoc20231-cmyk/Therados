from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from therados.db.session import get_db
from therados.models.domain_models import CandidateIntervention, PharmacologyAssessment, SafetyAssessment
from therados.schemas.domain_schemas import CandidateRead

router = APIRouter(prefix="/candidates", tags=["Candidate Interventions"])

@router.get("", response_model=List[CandidateRead])
async def list_candidates(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(CandidateIntervention))
    candidates = res.scalars().all()

    results = []
    for c in candidates:
        pharm_res = await db.execute(select(PharmacologyAssessment).where(PharmacologyAssessment.candidate_id == c.id))
        pharm = pharm_res.scalar_one_or_none()

        safety_res = await db.execute(select(SafetyAssessment).where(SafetyAssessment.candidate_id == c.id))
        safety = safety_res.scalar_one_or_none()

        results.append(CandidateRead(
            id=c.id,
            program_id=c.program_id,
            name=c.name,
            smiles=c.smiles,
            modality=c.modality,
            primary_target=c.primary_target,
            cpi_score=c.cpi_score,
            novelty_score=c.novelty_score,
            overall_status=c.overall_status,
            molecular_weight=pharm.molecular_weight if pharm else None,
            clogp=pharm.clogp if pharm else None,
            safety_gate_passed=safety.safety_gate_passed if safety else True,
            docking_status=pharm.docking_status if pharm else "Provider not configured",
            docking_score_kcal_mol=pharm.docking_score_kcal_mol if pharm else None
        ))
    return results
