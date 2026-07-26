from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(),
):

    return await service.chat(
        user_id=current_user.id,
        request=request,
    )