from agent.brain.brain import AgentBrain
from agent.conversation.manager import ConversationManager

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)


class ChatService:

    def __init__(
        self,
        brain: AgentBrain,
        conversation_manager: ConversationManager,
    ):
        self._brain = brain
        self._conversation_manager = conversation_manager

    async def chat(
        self,
        *,
        user_id: int,
        request: ChatRequest,
    ) -> ChatResponse:

        # Create conversation if needed
        if request.conversation_id is None:

            conversation = await self._conversation_manager.create(
                user_id=user_id,
                title="New Chat",
            )

            conversation_id = conversation.conversation_id

        else:

            conversation_id = request.conversation_id

        # Save user message
        await self._conversation_manager.append_user_message(
            conversation_id=conversation_id,
            content=request.message,
        )

        # Run agent
        result = await self._brain.run(
            user_input=request.message,
        )

        # Save assistant message
        await self._conversation_manager.append_assistant_message(
            conversation_id=conversation_id,
            content=result.response,
        )

        return ChatResponse(
            conversation_id=conversation_id,
            response=result.response,
        )