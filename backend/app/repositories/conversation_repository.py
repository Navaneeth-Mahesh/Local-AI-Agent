from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation


class ConversationRepository:
    """
    Handles all database operations related to conversations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        *,
        title: str,
        user_id: int,
    ) -> Conversation:
        conversation = Conversation(
            title=title,
            user_id=user_id,
        )

        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)

        return conversation

    async def get_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:

        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_user(
        self,
        user_id: int,
    ) -> list[Conversation]:

        result = await self.db.execute(
            select(Conversation)
            .where(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.created_at.desc()
            )
        )

        return list(result.scalars().all())

    async def update_title(
        self,
        conversation: Conversation,
        *,
        title: str,
    ) -> Conversation:

        conversation.title = title

        await self.db.commit()
        await self.db.refresh(conversation)

        return conversation

    async def delete(
        self,
        conversation: Conversation,
    ) -> None:

        await self.db.delete(conversation)
        await self.db.commit()