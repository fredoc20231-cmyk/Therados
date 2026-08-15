from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any

from therados.db.session import get_db
from therados.models.domain_models import AuditEvent

router = APIRouter(prefix="/audit", tags=["Audit Trail & Governance"])

@router.get("", response_model=None)
async def get_audit_trail(db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    res = await db.execute(select(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(100))
    events = res.scalars().all()
    return [
        {
            "id": e.id,
            "user_id": e.user_id,
            "action": e.action,
            "entity_type": e.entity_type,
            "entity_id": e.entity_id,
            "payload": e.payload,
            "timestamp": e.timestamp.isoformat()
        }
        for e in events
    ]
