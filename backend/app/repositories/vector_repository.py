import math
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.memory_vector import MemoryVector


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
    ) -> MemoryVector:
        stmt = select(MemoryVector).where(MemoryVector.memory_id == memory_id)
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.embedding = vector
            memory_vec = existing
        else:
            memory_vec = MemoryVector(
                memory_id=memory_id,
                embedding=vector,
            )
            self.db.add(memory_vec)

        await self.db.commit()
        await self.db.refresh(memory_vec)
        return memory_vec

    async def similarity_search(
        self,
        query_vector: list[float],
        *,
        limit: int = 5,
    ) -> list[MemoryVector]:
        # Try pgvector cosine distance if supported by DB dialect
        try:
            stmt = (
                select(MemoryVector)
                .order_by(
                    MemoryVector.embedding.cosine_distance(query_vector)
                )
                .limit(limit)
            )
            result = await self.db.scalars(stmt)
            return list(result.all())
        except Exception:
            # Python fallback for SQLite or non-pgvector environments
            stmt = select(MemoryVector)
            result = await self.db.scalars(stmt)
            all_vectors = list(result.all())

            def cosine_similarity(v1: list[float], v2: list[float]) -> float:
                if not v1 or not v2 or len(v1) != len(v2):
                    return 0.0
                dot = sum(a * b for a, b in zip(v1, v2))
                norm1 = math.sqrt(sum(a * a for a in v1))
                norm2 = math.sqrt(sum(b * b for b in v2))
                return dot / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0.0

            scored = [
                (vec, cosine_similarity(query_vector, vec.embedding))
                for vec in all_vectors
                if vec.embedding is not None
            ]
            scored.sort(key=lambda x: x[1], reverse=True)
            return [vec for vec, score in scored[:limit]]