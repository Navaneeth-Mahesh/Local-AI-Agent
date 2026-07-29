from agent.embeddings.interfaces import (
    BaseEmbeddingService,
)


class EmbeddingService:

    def __init__(
        self,
        provider: BaseEmbeddingService,
    ):
        self._provider = provider

    async def embed(
        self,
        text: str,
    ):
        return await self._provider.embed(
            text
        )