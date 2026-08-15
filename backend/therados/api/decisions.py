from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from therados.db.session import get_db
from therados.models.domain_models import Decision, TherapeuticHypothesis, DigitalTwinSnapshot, User
from therados.schemas.domain_schemas import DecisionRead, DecisionCreate
from therados.api.auth import get_current_user

router = APIRouter(prefix="/decisions", tags=["Decisions & Governance"])

@router.get("", response_model=List[DecisionRead])
async def list_decisions(db: AsyncSession = Depends(get_db)) -> List[DecisionRead]:
    res = await db.execute(select(Decision).order_by(Decision.created_at.desc()))
    decisions = res.scalars().all()
    return [DecisionRead.model_validate(d) for d in decisions]

@router.post("", response_model=DecisionRead)
async def record_decision(
    dec_in: DecisionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DecisionRead:
    res = await db.execute(select(TherapeuticHypothesis).where(TherapeuticHypothesis.id == dec_in.hypothesis_id))
    hypo = res.scalar_one_or_none()
    if not hypo:
        raise HTTPException(status_code=404, detail="Hypothesis not found")

    decision = Decision(
        hypothesis_id=dec_in.hypothesis_id,
        outcome=dec_in.outcome,
        rationale=dec_in.rationale,
        reviewer_id=current_user.id
    )
    db.add(decision)

    hypo.status = dec_in.outcome.value.lower()

    twins_res = await db.execute(
        select(DigitalTwinSnapshot)
        .where(DigitalTwinSnapshot.program_id == hypo.program_id)
        .order_by(DigitalTwinSnapshot.snapshot_index.desc())
    )
    last_twin = twins_res.scalars().first()
    next_idx = last_twin.snapshot_index + 1 if last_twin else 1

    twin = DigitalTwinSnapshot(
        program_id=hypo.program_id,
        snapshot_index=next_idx,
        trigger_event=f"Decision Recorded: {dec_in.outcome.value}",
        program_state={
            "hypothesis_id": hypo.id,
            "hypothesis_title": hypo.title,
            "outcome": dec_in.outcome.value,
            "rationale": dec_in.rationale
        }
    )
    db.add(twin)

    await db.commit()
    await db.refresh(decision)
    return DecisionRead.model_validate(decision)
