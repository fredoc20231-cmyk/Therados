from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from therados.db.session import get_db
from therados.models.domain_models import ExperimentPlan, ProofObligation, AlternativeMechanism
from therados.schemas.domain_schemas import ExperimentPlanRead
from scientific.experiments.voi_designer import ValueOfInformationDesigner

router = APIRouter(prefix="/experiments", tags=["Inverse Experiment Designer"])
voi_designer = ValueOfInformationDesigner()

@router.get("", response_model=List[ExperimentPlanRead])
async def list_experiment_plans(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ExperimentPlan))
    return res.scalars().all()

@router.post("/recommend/{hypothesis_id}")
async def recommend_experiment(hypothesis_id: str, db: AsyncSession = Depends(get_db)):
    pos_res = await db.execute(select(ProofObligation).where(ProofObligation.hypothesis_id == hypothesis_id))
    pos = [{"id": p.id, "proposition": p.proposition, "state": p.state} for p in pos_res.scalars().all()]

    alts_res = await db.execute(select(AlternativeMechanism).where(AlternativeMechanism.hypothesis_id == hypothesis_id))
    alts = [{"mechanism_name": a.mechanism_name, "evidence_support": a.evidence_support} for a in alts_res.scalars().all()]

    return voi_designer.recommend_experiment(hypothesis_id, pos, alts)
