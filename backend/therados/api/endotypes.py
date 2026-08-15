from fastapi import APIRouter
from scientific.endotypes.endotype_engine import EndotypeEngine

router = APIRouter(prefix="/endotypes", tags=["Disease Endotypes"])
endotype_engine = EndotypeEngine()

@router.get("")
async def get_endotypes():
    return endotype_engine.assign_endotype()
