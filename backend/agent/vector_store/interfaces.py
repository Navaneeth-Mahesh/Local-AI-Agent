from abc import ABC, abstractmethod

from agent.vector_store.models import (
    VectorRecord,
)


class BaseVectorStore(ABC):

    @abstractmethod
    async def upsert(
        self,
        record: VectorRecord,
    ) -> None:
        ...

    @abstractmethod
    async def similarity_search(
        self,
        vector: list[float],
        *,
        limit: int = 5,
    ) -> list[VectorRecord]:
        ...