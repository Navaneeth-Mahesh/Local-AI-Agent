from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user, get_ai_provider_service
from app.models.user import User
from app.schemas.ai_provider import (
    AIProviderCreate,
    AIProviderResponse,
)
from app.services.ai_provider_service import AIProviderService

router = APIRouter(
    prefix="/ai-provider",
    tags=["AI Provider"],
)


@router.get(
    "/",
    response_model=AIProviderResponse,
)
async def get_provider(
    current_user: User = Depends(get_current_user),
    service: AIProviderService = Depends(get_ai_provider_service),
):
    provider = await service.get_provider(current_user.id)
    if not provider:
        return AIProviderResponse(
            provider="gemini",
            api_key="",
            model="gemini-2.5-flash",
            temperature=0.7,
        )
    return provider


@router.post(
    "/",
    response_model=AIProviderResponse,
)
async def save_provider(
    data: AIProviderCreate,
    current_user: User = Depends(get_current_user),
    service: AIProviderService = Depends(get_ai_provider_service),
):
    return await service.save_provider(
        current_user.id,
        data,
    )