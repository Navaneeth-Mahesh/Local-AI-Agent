from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AIProvider(Base):
    __tablename__ = "ai_providers"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(30),
        default="gemini",
    )

    api_key: Mapped[str] = mapped_column(
        String(255),
    )

    model: Mapped[str] = mapped_column(
        String(100),
        default="gemini-2.5-flash",
    )

    temperature: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    user = relationship(
        "User",
        back_populates="ai_provider",
    )