from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
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
async def list_evidence(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(EvidenceRecord).order_by(EvidenceRecord.retrieval_timestamp.desc()))
    return res.scalars().all()

@router.post("/ingest", response_model=EvidenceRecordRead)
async def ingest_evidence(record_in: EvidenceRecordCreate, db: AsyncSession = Depends(get_db)):
    # Find or create source
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
    return record

@router.get("/independence-score")
async def evaluate_independence(db: AsyncSession = Depends(get_db)):
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
