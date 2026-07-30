from agent.embeddings.service import EmbeddingService
from agent.vector_store.interfaces import BaseVectorStore


class DocumentRetriever:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: BaseVectorStore,
    ):
        self._embedding_service = embedding_service
        self._vector_store = vector_store

    async def retrieve(
        self,
        *,
        query: str,
        limit: int = 5,
    ):

        embedding = await self._embedding_service.embed(
            query
        )

        return await self._vector_store.similarity_search(
            embedding.vector,
            limit=limit,
        )