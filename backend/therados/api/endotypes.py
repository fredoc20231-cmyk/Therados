from fastapi import APIRouter
from typing import Dict, Any
from scientific.endotypes.endotype_engine import EndotypeEngine

router = APIRouter(prefix="/endotypes", tags=["Disease Endotypes"])
endotype_engine = EndotypeEngine()

@router.get("")
async def get_endotypes() -> Dict[str, Any]:
    return endotype_engine.assign_endotype()
