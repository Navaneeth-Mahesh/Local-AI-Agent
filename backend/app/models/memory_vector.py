from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from pgvector.sqlalchemy import Vector

from app.database.base import Base


class MemoryVector(Base):

    __tablename__ = "memory_vectors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    memory_id: Mapped[int] = mapped_column(
        ForeignKey(
            "long_term_memories.id",
            ondelete="CASCADE",
        ),
        unique=True,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(768),
    )