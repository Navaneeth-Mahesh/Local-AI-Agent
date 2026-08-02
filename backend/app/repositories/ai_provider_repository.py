from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ai_provider import AIProvider


class AIProviderRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int) -> AIProvider | None:
        statement = select(AIProvider).where(AIProvider.user_id == user_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def save(self, provider: AIProvider) -> AIProvider:
        self.db.add(provider)
        await self.db.commit()
        await self.db.refresh(provider)
        return provider

    async def update(self, provider: AIProvider) -> AIProvider:
        await self.db.commit()
        await self.db.refresh(provider)
        return provider