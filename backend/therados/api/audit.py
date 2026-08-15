from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from therados.db.session import get_db
from therados.models.domain_models import AuditEvent

router = APIRouter(prefix="/audit", tags=["Audit Trail & Governance"])

@router.get("")
async def get_audit_trail(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(100))
    events = res.scalars().all()
    return events
