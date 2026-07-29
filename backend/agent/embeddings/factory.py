from agent.embeddings.service import (
    EmbeddingService,
)


class EmbeddingFactory:

    @staticmethod
    def create(
        provider,
    ) -> EmbeddingService:

        return EmbeddingService(
            provider=provider,
        )