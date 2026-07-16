from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai_provider import AIProvider


class AIProviderRepository:

    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int):
        statement = (
            select(AIProvider)
            .where(AIProvider.user_id == user_id)
        )
        return self.db.scalar(statement)

    def save(self, provider: AIProvider):
        self.db.add(provider)
        self.db.commit()
        self.db.refresh(provider)
        return provider

    def update(self, provider: AIProvider):
        self.db.commit()
        self.db.refresh(provider)
        return provider