from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any, cast

from therados.db.session import get_db
from therados.models.domain_models import TherapeuticHypothesis, AlternativeMechanism
from therados.schemas.domain_schemas import HypothesisRead, HypothesisCreate
from scientific.hypothesis_compiler.compiler import HypothesisCompiler
from scientific.falsification.falsification_engine import AdversarialFalsificationEngine

router = APIRouter(prefix="/hypotheses", tags=["Therapeutic Hypotheses"])
compiler = HypothesisCompiler()
falsification_engine = AdversarialFalsificationEngine()

@router.get("", response_model=List[HypothesisRead])
async def list_hypotheses(db: AsyncSession = Depends(get_db)) -> List[HypothesisRead]:
    res = await db.execute(select(TherapeuticHypothesis))
    hypos = res.scalars().all()
    return [HypothesisRead.model_validate(h) for h in hypos]

@router.post("", response_model=HypothesisRead)
async def create_hypothesis(hypo_in: HypothesisCreate, db: AsyncSession = Depends(get_db)) -> HypothesisRead:
    hypo = TherapeuticHypothesis(
        program_id=hypo_in.program_id,
        title=hypo_in.title,
        intervention_name=hypo_in.intervention_name,
        intended_target=hypo_in.intended_target,
        intended_action=hypo_in.intended_action,
        cellular_context=hypo_in.cellular_context,
        disease_endotype=hypo_in.disease_endotype,
        genomic_background=hypo_in.genomic_background,
        predictive_biomarkers=hypo_in.predictive_biomarkers,
        dose_exposure_regime=hypo_in.dose_exposure_regime,
        schedule_duration=hypo_in.schedule_duration,
        safety_constraints=hypo_in.safety_constraints or {}
    )
    db.add(hypo)
    await db.commit()
    await db.refresh(hypo)
    return HypothesisRead.model_validate(hypo)

@router.post("/{hypothesis_id}/compile")
async def compile_hypothesis(hypothesis_id: str, db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    res = await db.execute(select(TherapeuticHypothesis).where(TherapeuticHypothesis.id == hypothesis_id))
    hypo = res.scalar_one_or_none()
    if not hypo:
        raise HTTPException(status_code=404, detail="Hypothesis not found")

    dossier = compiler.compile_hypothesis(
        hypothesis_id=hypo.id,
        intervention=hypo.intervention_name,
        target=hypo.intended_target,
        action=hypo.intended_action,
        cellular_context=hypo.cellular_context,
        disease_endotype=hypo.disease_endotype,
        genomic_background=hypo.genomic_background,
        predictive_biomarkers=hypo.predictive_biomarkers
    )

    hypo.status = "compiled"
    await db.commit()
    return cast(Dict[str, Any], dossier.model_dump())

@router.post("/{hypothesis_id}/falsify")
async def falsify_hypothesis(hypothesis_id: str, db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    res = await db.execute(select(TherapeuticHypothesis).where(TherapeuticHypothesis.id == hypothesis_id))
    hypo = res.scalar_one_or_none()
    if not hypo:
        raise HTTPException(status_code=404, detail="Hypothesis not found")

    alts_res = await db.execute(select(AlternativeMechanism).where(AlternativeMechanism.hypothesis_id == hypothesis_id))
    alts = alts_res.scalars().all()
    alts_data = [
        {
            "mechanism_name": a.mechanism_name,
            "description": a.description,
            "evidence_support": a.evidence_support,
            "discriminating_assay": a.discriminating_assay
        }
        for a in alts
    ]

    dossier = falsification_engine.generate_falsification_dossier(
        hypothesis_id=hypo.id,
        hypothesis_title=hypo.title,
        alternative_mechanisms=alts_data
    )
    return cast(Dict[str, Any], dossier.model_dump())
