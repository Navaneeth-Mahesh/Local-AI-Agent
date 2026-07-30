from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class IndexedFile:

    path: Path

    file_name: str

    extension: str

    size: int

    modified_at: datetime

    sha256: str


@dataclass(slots=True)
class Document:

    path: Path

    title: str

    content: str

    metadata: dict