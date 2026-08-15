from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/integrations", tags=["Integrations & Connectors"])

@router.get("")
async def list_integrations() -> List[Dict[str, Any]]:
    return [
        {"name": "Open Targets Platform API", "type": "Public Target-Disease Evidence", "status": "HEALTHY", "requires_credentials": False},
        {"name": "ChEMBL Bioactivity Database API", "type": "Bioassay & Small Molecule Binding", "status": "HEALTHY", "requires_credentials": False},
        {"name": "UniProt Knowledgebase REST API", "type": "Protein Annotation & Variants", "status": "HEALTHY", "requires_credentials": False},
        {"name": "PubChem PUG REST", "type": "Chemical Structures & Properties", "status": "HEALTHY", "requires_credentials": False},
        {"name": "DrugBank DB (Licensed)", "type": "Approved & Investigational Drugs", "status": "REQUIRES_CREDENTIALS", "requires_credentials": True}
    ]
