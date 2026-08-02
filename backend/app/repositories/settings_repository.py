from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_settings import UserSettings


class SettingsRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int) -> UserSettings | None:
        statement = select(UserSettings).where(UserSettings.user_id == user_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, settings: UserSettings) -> UserSettings:
        self.db.add(settings)
        await self.db.commit()
        await self.db.refresh(settings)
        return settings

    async def update(self, settings: UserSettings) -> UserSettings:
        await self.db.commit()
        await self.db.refresh(settings)
        return settings