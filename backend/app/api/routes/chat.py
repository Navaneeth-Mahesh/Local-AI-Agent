from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_current_user, get_chat_service, get_agent_brain
from app.models.user import User
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.chat_service import ChatService
from agent.brain.brain import AgentBrain
from agent.streaming.service import StreamingService

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
    current_user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    return await service.chat(
        user_id=current_user.id,
        request=request,
    )


@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    brain: AgentBrain = Depends(get_agent_brain),
):
    streaming_service = StreamingService()

    async def token_generator():
        response = await brain.run(
            user_input=request.message,
        )
        yield response.response

    generator = streaming_service.stream(token_generator())

    return StreamingResponse(
        generator,
        media_type="text/event-stream",
    )