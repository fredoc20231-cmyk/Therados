from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from typing import Dict

from therados.db.session import get_db

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "TheraDOS Core API", "version": "1.0.0"}

@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        return {"status": "unready", "database": str(e)}
