from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


class MessageRepository:
    """
    Handles all database operations related to messages.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        *,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)

        await self.db.commit()
        await self.db.refresh(message)

        return message

    async def get_by_id(
        self,
        message_id: int,
    ) -> Message | None:

        result = await self.db.execute(
            select(Message).where(
                Message.id == message_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_conversation(
        self,
        conversation_id: int,
    ) -> list[Message]:

        result = await self.db.execute(
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at.asc()
            )
        )

        return list(result.scalars().all())

    async def get_recent_messages(
        self,
        conversation_id: int,
        limit: int = 20,
    ) -> list[Message]:

        result = await self.db.execute(
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at.desc()
            )
            .limit(limit)
        )

        return list(
            reversed(
                result.scalars().all()
            )
        )

    async def delete(
        self,
        message: Message,
    ) -> None:

        await self.db.delete(message)
        await self.db.commit()