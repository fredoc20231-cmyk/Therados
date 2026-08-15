from fastapi import APIRouter
from typing import List, Dict, Any
from therados.config.settings import settings

router = APIRouter(prefix="/models", tags=["Model Registry & Providers"])

@router.get("")
async def get_model_providers() -> List[Dict[str, Any]]:
    provider_status = [
        {
            "provider_name": "OpenAI LLM",
            "is_configured": bool(settings.OPENAI_API_KEY),
            "status_reason": "Active" if settings.OPENAI_API_KEY else "OPENAI_API_KEY environment variable not configured"
        },
        {
            "provider_name": "Anthropic Claude",
            "is_configured": bool(settings.ANTHROPIC_API_KEY),
            "status_reason": "Active" if settings.ANTHROPIC_API_KEY else "ANTHROPIC_API_KEY environment variable not configured"
        },
        {
            "provider_name": "RDKit Cheminformatics",
            "is_configured": True,
            "status_reason": "Active (Local RDKit engine installed)"
        },
        {
            "provider_name": "AutoDock Vina Docking",
            "is_configured": bool(settings.AUTODOCK_VINA_PATH),
            "status_reason": "Active" if settings.AUTODOCK_VINA_PATH else "AUTODOCK_VINA_PATH executable not configured"
        }
    ]
    return provider_status
