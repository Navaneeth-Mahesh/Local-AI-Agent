from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_settings import UserSettings
from app.repositories.settings_repository import SettingsRepository
from app.schemas.settings import UserSettingsUpdate, UserSettingsResponse


class SettingsService:

    def __init__(self, db: AsyncSession):
        self.repository = SettingsRepository(db)

    async def get_settings(self, user_id: int) -> UserSettings:
        settings = await self.repository.get(user_id)

        if settings:
            return settings

        settings = UserSettings(user_id=user_id)
        return await self.repository.create(settings)

    async def update_settings(
        self,
        user_id: int,
        data: UserSettingsUpdate,
    ) -> UserSettings:
        settings = await self.get_settings(user_id)

        if data.theme is not None:
            settings.theme = data.theme
        if data.ai_provider is not None:
            settings.ai_provider = data.ai_provider
        if data.default_model is not None:
            settings.default_model = data.default_model
        if data.language is not None:
            settings.language = data.language
        if data.voice_enabled is not None:
            settings.voice_enabled = data.voice_enabled

        return await self.repository.update(settings)
