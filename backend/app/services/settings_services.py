from sqlalchemy.orm import Session

from app.models.user_settings import UserSettings
from app.repositories.settings_repository import SettingsRepository


class SettingsService:

    def __init__(self, db: Session):
        self.repository = SettingsRepository(db)

    def get_settings(self, user_id: int):
        settings = self.repository.get(user_id)

        if settings:
            return settings

        settings = UserSettings(user_id=user_id)

        return self.repository.create(settings)

    def update_settings(
        self,
        user_id: int,
        data,
    ):
        settings = self.get_settings(user_id)

        settings.theme = data.theme
        settings.ai_provider = data.ai_provider
        settings.default_model = data.default_model
        settings.language = data.language
        settings.voice_enabled = data.voice_enabled

        return self.repository.update(settings)