from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from therados.db.session import get_db
from therados.models.domain_models import TherapeuticProgram, DigitalTwinSnapshot, User
from therados.schemas.domain_schemas import ProgramRead, ProgramCreate, DigitalTwinSnapshotRead
from therados.api.auth import get_current_user

router = APIRouter(prefix="/programs", tags=["Therapeutic Programs"])

@router.get("", response_model=List[ProgramRead])
async def list_programs(db: AsyncSession = Depends(get_db)) -> List[ProgramRead]:
    res = await db.execute(select(TherapeuticProgram))
    programs = res.scalars().all()
    return [ProgramRead.model_validate(p) for p in programs]

@router.post("", response_model=ProgramRead)
async def create_program(
    program_in: ProgramCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ProgramRead:
    program = TherapeuticProgram(
        project_id=program_in.project_id,
        disease=program_in.disease,
        indication=program_in.indication,
        patient_context=program_in.patient_context,
        disease_stage=program_in.disease_stage,
        treatment_context=program_in.treatment_context,
        program_objective=program_in.program_objective,
        constraints=program_in.constraints or {}
    )
    db.add(program)
    await db.commit()
    await db.refresh(program)
    return ProgramRead.model_validate(program)

@router.get("/{program_id}", response_model=ProgramRead)
async def get_program(program_id: str, db: AsyncSession = Depends(get_db)) -> ProgramRead:
    res = await db.execute(select(TherapeuticProgram).where(TherapeuticProgram.id == program_id))
    program = res.scalar_one_or_none()
    if not program:
        raise HTTPException(status_code=404, detail="Therapeutic program not found")
    return ProgramRead.model_validate(program)

@router.get("/{program_id}/digital-twin", response_model=List[DigitalTwinSnapshotRead])
async def get_digital_twin_timeline(program_id: str, db: AsyncSession = Depends(get_db)) -> List[DigitalTwinSnapshotRead]:
    res = await db.execute(
        select(DigitalTwinSnapshot)
        .where(DigitalTwinSnapshot.program_id == program_id)
        .order_by(DigitalTwinSnapshot.snapshot_index.asc())
    )
    snapshots = res.scalars().all()
    return [DigitalTwinSnapshotRead.model_validate(s) for p in [snapshots] for s in p]
