from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any
import hashlib

from therados.db.session import get_db
from therados.models.domain_models import EvidenceRecord, EvidenceSource, EvidenceClaim
from therados.schemas.domain_schemas import EvidenceRecordRead, EvidenceRecordCreate
from scientific.evidence.independence_engine import EvidenceIndependenceEngine

router = APIRouter(prefix="/evidence", tags=["Evidence & Provenance"])
independence_engine = EvidenceIndependenceEngine()

@router.get("", response_model=List[EvidenceRecordRead])
async def list_evidence(
    include_synthetic: bool = Query(default=False, description="Set to True to include tutorial synthetic evidence"),
    db: AsyncSession = Depends(get_db)
) -> List[EvidenceRecordRead]:
    query = select(EvidenceRecord)
    if not include_synthetic:
        query = query.where(EvidenceRecord.is_synthetic.is_(False))
    query = query.order_by(EvidenceRecord.retrieval_timestamp.desc())

    res = await db.execute(query)
    records = res.scalars().all()
    return [EvidenceRecordRead.model_validate(r) for r in records]

@router.post("/ingest", response_model=EvidenceRecordRead)
async def ingest_evidence(
    record_in: EvidenceRecordCreate,
    is_tutorial_project: bool = Query(default=False, description="Set to True only if ingesting into a synthetic tutorial project"),
    db: AsyncSession = Depends(get_db)
) -> EvidenceRecordRead:
    if record_in.is_synthetic and not is_tutorial_project:
        raise HTTPException(
            status_code=400,
            detail="Synthetic tutorial evidence cannot be ingested into a non-tutorial production project."
        )

    res = await db.execute(select(EvidenceSource).where(EvidenceSource.name == record_in.source_name))
    source = res.scalar_one_or_none()
    if not source:
        source = EvidenceSource(name=record_in.source_name, source_type="UserUpload")
        db.add(source)
        await db.flush()

    payload_str = str(record_in.normalized_payload)
    checksum = hashlib.sha256(payload_str.encode()).hexdigest()

    record = EvidenceRecord(
        source_id=source.id,
        external_id=record_in.external_id,
        evidence_type=record_in.evidence_type,
        evidence_maturity=record_in.evidence_maturity,
        normalized_payload=record_in.normalized_payload,
        checksum=checksum,
        quality_score=record_in.quality_score,
        is_synthetic=record_in.is_synthetic
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return EvidenceRecordRead.model_validate(record)

@router.get("/independence-score")
async def evaluate_independence(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    res = await db.execute(select(EvidenceClaim))
    claims = res.scalars().all()
    claims_data = [
        {
            "id": c.id,
            "evidence_record_id": c.evidence_record_id,
            "external_id": c.evidence_record_id,
            "source_name": "Ingested Source",
            "quality_score": 0.9,
            "evidence_maturity": c.evidence_maturity
        }
        for c in claims
    ]
    return independence_engine.compute_independent_support(claims_data)
