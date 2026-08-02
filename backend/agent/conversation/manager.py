from agent.conversation.interfaces import (
    BaseConversationManager,
)
from agent.conversation.mapper import (
    ConversationMapper,
)
from agent.conversation.models import (
    ConversationContext,
)
from app.repositories.conversation_repository import (
    ConversationRepository,
)
from app.repositories.message_repository import (
    MessageRepository,
)


class ConversationManager(BaseConversationManager):

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
    ) -> None:
        self._conversation_repository = conversation_repository
        self._message_repository = message_repository

    async def load(
        self,
        conversation_id: int,
    ) -> ConversationContext:
        conversation = await self._conversation_repository.get_by_id(
            conversation_id
        )
        return ConversationMapper.to_domain(conversation)

    async def append_user_message(
        self,
        conversation_id: int,
        content: str,
    ) -> None:
        await self._message_repository.create(
            conversation_id=conversation_id,
            role="user",
            content=content,
        )

    async def append_assistant_message(
        self,
        conversation_id: int,
        content: str,
    ) -> None:
        await self._message_repository.create(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
        )

    async def create(
        self,
        *,
        user_id: int,
        title: str,
    ) -> ConversationContext:
        conversation = await self._conversation_repository.create(
            title=title,
            user_id=user_id,
        )
        return ConversationMapper.to_domain(conversation)