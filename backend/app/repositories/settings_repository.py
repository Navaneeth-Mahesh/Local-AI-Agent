from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_settings import UserSettings


class SettingsRepository:

    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int):
        statement = (
            select(UserSettings)
            .where(UserSettings.user_id == user_id)
        )
        return self.db.scalar(statement)

    def create(self, settings: UserSettings):
        self.db.add(settings)
        self.db.commit()
        self.db.refresh(settings)
        return settings

    def update(self, settings: UserSettings):
        self.db.commit()
        self.db.refresh(settings)
        return settings