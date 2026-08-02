from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class MemoryFact:

    id: int | None = None

    user_id: int = 0

    content: str = ""

    importance: float = 0.5

    source_message_id: int | None = None

    created_at: datetime | None = None