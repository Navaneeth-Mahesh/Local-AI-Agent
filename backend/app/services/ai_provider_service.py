from sqlalchemy.orm import Session

from app.models.ai_provider import AIProvider
from app.repositories.ai_provider_repository import (
    AIProviderRepository,
)


class AIProviderService:

    def __init__(self, db: Session):
        self.repository = AIProviderRepository(db)

    def get_provider(
        self,
        user_id: int,
    ):
        return self.repository.get(user_id)

    def save_provider(
        self,
        user_id: int,
        data,
    ):
        provider = self.repository.get(user_id)

        if provider:
            provider.provider = data.provider
            provider.api_key = data.api_key
            provider.model = data.model
            provider.temperature = data.temperature

            return self.repository.update(provider)

        provider = AIProvider(
            user_id=user_id,
            provider=data.provider,
            api_key=data.api_key,
            model=data.model,
            temperature=data.temperature,
        )

        return self.repository.save(provider)