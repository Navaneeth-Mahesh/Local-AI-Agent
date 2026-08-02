from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.message import Message


class MessageRepository:

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
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

    async def get_by_conversation(
        self,
        conversation_id: int,
        limit: int = 50,
    ) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        result = await self.db.scalars(stmt)
        return list(result.all())
