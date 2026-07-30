from agent.vector_store.models import (
    VectorRecord,
)

from app.models.memory_vector import (
    MemoryVector,
)


class VectorMapper:

    @staticmethod
    def to_domain(
        model: MemoryVector,
    ) -> VectorRecord:

        return VectorRecord(
            id=model.id,
            user_id=0,
            vector=model.embedding,
            metadata={},
        )