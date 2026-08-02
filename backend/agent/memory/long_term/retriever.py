from agent.embeddings.service import EmbeddingService
from agent.vector_store.interfaces import BaseVectorStore
from agent.memory.long_term.manager import LongTermMemoryManager


class MemoryRetriever:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: BaseVectorStore,
        memory_manager: LongTermMemoryManager,
    ):
        self._embedding_service = embedding_service
        self._vector_store = vector_store
        self._memory_manager = memory_manager

    async def retrieve(
        self,
        *,
        user_id: int,
        query: str,
        limit: int = 5,
    ):

        embedding = await self._embedding_service.embed(
            query
        )

        vectors = await self._vector_store.similarity_search(
            embedding.vector,
            limit=limit,
        )

        memory_ids = [
            vector.metadata["memory_id"]
            for vector in vectors
        ]

        return await self._memory_manager.get_by_ids(
            user_id=user_id,
            ids=memory_ids,
        )