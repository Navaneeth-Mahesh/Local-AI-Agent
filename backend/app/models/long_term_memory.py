from datetime import datetime, UTC
from sqlalchemy import ForeignKey, Float, Text, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class LongTermMemory(Base):
    __tablename__ = "long_term_memories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    importance: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    source_message_id: Mapped[int | None] = mapped_column(ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    vector: Mapped["MemoryVector"] = relationship(
        "MemoryVector",
        back_populates="memory",
        cascade="all, delete-orphan",
        uselist=False,
    )
