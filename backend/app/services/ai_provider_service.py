from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_provider import AIProvider
from app.repositories.ai_provider_repository import AIProviderRepository
from app.schemas.ai_provider import AIProviderCreate


class AIProviderService:

    def __init__(self, db: AsyncSession):
        self.repository = AIProviderRepository(db)

    async def get_provider(
        self,
        user_id: int,
    ) -> AIProvider | None:
        return await self.repository.get(user_id)

    async def save_provider(
        self,
        user_id: int,
        data: AIProviderCreate,
    ) -> AIProvider:
        provider = await self.repository.get(user_id)

        if provider:
            provider.provider = data.provider
            provider.api_key = data.api_key
            provider.model = data.model
            provider.temperature = data.temperature
            return await self.repository.update(provider)

        provider = AIProvider(
            user_id=user_id,
            provider=data.provider,
            api_key=data.api_key,
            model=data.model,
            temperature=data.temperature,
        )

        return await self.repository.save(provider)