from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory_vector import (
    MemoryVector,
)


class VectorRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def upsert(
        self,
        *,
        memory_id: int,
        vector: list[float],
    ):

        existing = await self.db.scalar(
            select(
                MemoryVector
            ).where(
                MemoryVector.memory_id
                == memory_id
            )
        )

        if existing:

            existing.embedding = vector

        else:

            self.db.add(
                MemoryVector(
                    memory_id=memory_id,
                    embedding=vector,
                )
            )

        await self.db.commit()
        from sqlalchemy import select


async def similarity_search(
    self,
    query_vector,
    *,
    limit=5,
):

    stmt = (
        select(MemoryVector)
        .order_by(
            MemoryVector.embedding.cosine_distance(
                query_vector
            )
        )
        .limit(limit)
    )

    result = await self.db.scalars(stmt)

    return list(result)