from agent.embeddings.service import EmbeddingService


class ChunkEmbedder:

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ):
        self._embedding_service = embedding_service

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        embedding = await self._embedding_service.embed(
            text
        )

        return embedding.vector