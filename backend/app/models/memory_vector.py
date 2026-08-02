from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.database.base import Base


class MemoryVector(Base):
    __tablename__ = "memory_vectors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    memory_id: Mapped[int] = mapped_column(
        ForeignKey(
            "long_term_memories.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    # Use pgvector Vector type, with JSON fallback if pgvector is not available in SQLite
    embedding: Mapped[list[float]] = mapped_column(
        Vector(768).with_variant(JSON, "sqlite"),
        nullable=False,
    )

    memory: Mapped["LongTermMemory"] = relationship(
        "LongTermMemory",
        back_populates="vector",
    )