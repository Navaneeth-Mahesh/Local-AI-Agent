from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    BigInteger,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class IndexedFile(Base):
    __tablename__ = "indexed_files"

    id: Mapped[int] = mapped_column(primary_key=True)

    folder_id: Mapped[int] = mapped_column(
        ForeignKey(
            "indexed_folders.id",
            ondelete="CASCADE",
        )
    )

    path: Mapped[str] = mapped_column(
        String(2000),
        unique=True,
    )

    sha256: Mapped[str] = mapped_column(
        String(64),
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
    )

    last_modified: Mapped[datetime] = mapped_column(
        DateTime,
    )

    folder = relationship(
        "IndexedFolder",
        back_populates="files",
    )