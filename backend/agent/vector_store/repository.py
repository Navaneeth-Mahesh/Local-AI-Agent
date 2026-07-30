from agent.vector_store.interfaces import (
    BaseVectorStore,
)
from agent.vector_store.mapper import (
    VectorMapper,
)


class PgVectorStore(
    BaseVectorStore,
):

    def __init__(
        self,
        repository,
    ):
        self._repository = repository

    async def upsert(
        self,
        record,
    ):

        await self._repository.upsert(
            memory_id=record.id,
            vector=record.vector,
        )

    async def similarity_search(
        self,
        vector,
        *,
        limit=5,
    ):

        models = await self._repository.similarity_search(
            vector,
            limit=limit,
        )

        return [
            VectorMapper.to_domain(m)
            for m in models
        ]