from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.chat_service import ChatService
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
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

@router.post("/stream")
async def stream_chat():

    generator = streaming_service.stream(
        agent_executor.stream(state)
    )

    return StreamingResponse(
        generator,
        media_type="text/event-stream",
    )