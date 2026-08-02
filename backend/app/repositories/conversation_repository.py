from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation


class ConversationRepository:

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def get_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:
        stmt = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user(
        self,
        user_id: int,
    ) -> list[Conversation]:
        stmt = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

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