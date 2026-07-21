from app.models.conversation import Conversation
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    """
    Business logic for conversations.
    """

    def __init__(
        self,
        repository: ConversationRepository,
    ) -> None:
        self._repository = repository

    async def create_conversation(
        self,
        *,
        title: str,
        user_id: int,
    ) -> Conversation:

        return await self._repository.create(
            title=title,
            user_id=user_id,
        )

    async def get_conversation(
        self,
        conversation_id: int,
    ) -> Conversation | None:

        return await self._repository.get_by_id(
            conversation_id
        )

    async def get_user_conversations(
        self,
        user_id: int,
    ) -> list[Conversation]:

        return await self._repository.get_by_user(
            user_id
        )

    async def rename_conversation(
        self,
        conversation: Conversation,
        *,
        title: str,
    ) -> Conversation:

        title = title.strip()

        if not title:
            raise ValueError(
                "Conversation title cannot be empty."
            )

        return await self._repository.update_title(
            conversation,
            title=title,
        )

    async def delete_conversation(
        self,
        conversation: Conversation,
    ) -> None:

        await self._repository.delete(
            conversation
        )