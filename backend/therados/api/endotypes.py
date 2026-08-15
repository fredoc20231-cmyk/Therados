from fastapi import APIRouter
from typing import Dict, Any, cast
from scientific.endotypes.endotype_engine import EndotypeEngine

router = APIRouter(prefix="/endotypes", tags=["Disease Endotypes"])
endotype_engine = EndotypeEngine()

@router.get("")
async def get_endotypes() -> Dict[str, Any]:
    return cast(Dict[str, Any], endotype_engine.assign_endotype())
