from agent.adapters.gemini.embedding_provider import (
    GeminiEmbeddingProvider,
)
from agent.adapters.gemini.config import (
    DEFAULT_EMBEDDING_MODEL,
)
from agent.embeddings.service import (
    EmbeddingService,
)


class EmbeddingFactory:

    @staticmethod
    def create_gemini(
        api_key: str,
    ) -> EmbeddingService:

        provider = GeminiEmbeddingProvider(
            api_key=api_key,
            model=DEFAULT_EMBEDDING_MODEL,
        )

        return EmbeddingService(
            provider=provider,
        )