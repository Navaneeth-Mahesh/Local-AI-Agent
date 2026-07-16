from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    theme: Mapped[str] = mapped_column(
        String(20),
        default="dark",
    )

    ai_provider: Mapped[str] = mapped_column(
        String(30),
        default="gemini",
    )

    default_model: Mapped[str] = mapped_column(
        String(100),
        default="gemini-2.5-flash",
    )

    language: Mapped[str] = mapped_column(
        String(20),
        default="en",
    )

    voice_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    user = relationship("User", back_populates="settings")