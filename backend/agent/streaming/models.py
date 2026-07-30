from dataclasses import dataclass


@dataclass(slots=True)
class StreamEvent:
    event: str
    data: str