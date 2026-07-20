from fastapi import Depends
from app.core.config import settings
from agent.llm.enums import ProviderType
from agent.llm.factory import LLMFactory
from agent.llm.service import LLMService

def get_llm_service() -> LLMService:
    """
    FastAPI dependency.

    Later this will read the authenticated user's
    provider settings and API key from the database.
    """
    
    provider = LLMFactory.create(
        provider=ProviderType.GEMINI,
        api_key=settings.GEMINI_API_KEY,
    )
    return LLMService(provider)