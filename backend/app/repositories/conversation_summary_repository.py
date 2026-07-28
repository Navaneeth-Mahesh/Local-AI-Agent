from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation_summary import (
    ConversationSummary,
)


class ConversationSummaryRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get(
        self,
        conversation_id: int,
    ) -> ConversationSummary | None:

        stmt = select(
            ConversationSummary
        ).where(
            ConversationSummary.conversation_id
            == conversation_id
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def save(
        self,
        summary: ConversationSummary,
    ):

        self.db.add(summary)

        await self.db.commit()

        await self.db.refresh(summary)

        return summary
        