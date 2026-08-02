from google.genai import Client

from agent.adapters.gemini.embedding_mapper import (
    GeminiEmbeddingMapper,
)
from agent.embeddings.interfaces import (
    BaseEmbeddingService,
)
from agent.embeddings.models import (
    EmbeddingResult,
)


class GeminiEmbeddingProvider(BaseEmbeddingService):

    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        self._client = Client(
            api_key=api_key,
        )
        self._model = model

    async def embed(
        self,
        text: str,
    ) -> EmbeddingResult:
        response = await self._client.aio.models.embed_content(
            model=self._model,
            contents=text,
        )

        return GeminiEmbeddingMapper.to_domain(
            response
        )