from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class IndexedFile:
    """
    Domain model representing an indexed file.
    """

    path: Path

    file_name: str

    extension: str

    size: int

    modified_at: datetime

    sha256: str