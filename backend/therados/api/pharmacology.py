from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, cast

from scientific.pharmacology.rdkit_engine import RDKitEngine, AutoDockVinaAdapter
from scientific.pharmacology.safety_gate import HardSafetyGateEngine

router = APIRouter(prefix="/pharmacology", tags=["Pharmacology & Safety"])
rdkit_engine = RDKitEngine()
vina_adapter = AutoDockVinaAdapter()
safety_gate_engine = HardSafetyGateEngine()

class SmilesRequest(BaseModel):
    smiles: str

class DockingRequest(BaseModel):
    smiles: str
    target_pdb_id: str

@router.post("/evaluate-smiles")
async def evaluate_smiles(req: SmilesRequest) -> Dict[str, Any]:
    return cast(Dict[str, Any], rdkit_engine.evaluate_smiles(req.smiles))

@router.post("/dock")
async def run_docking(req: DockingRequest) -> Dict[str, Any]:
    return cast(Dict[str, Any], vina_adapter.run_docking(req.smiles, req.target_pdb_id))

@router.post("/safety-gate")
async def evaluate_safety_gate(
    herg: str = "LOW",
    hepato: str = "LOW",
    genotox: str = "LOW",
    free_conc: float = 100.0,
    required_ic50: float = 50.0
) -> Dict[str, Any]:
    return cast(Dict[str, Any], safety_gate_engine.evaluate_gates(
        herg_liability=herg,
        hepatotoxicity_liability=hepato,
        genotoxicity_liability=genotox,
        free_concentration_nm=free_conc,
        required_ic50_nm=required_ic50
    ))
