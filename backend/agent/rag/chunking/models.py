from dataclasses import dataclass


@dataclass(slots=True)
class DocumentChunk:

    id: int

    text: str

    chunk_index: int

    source: str

    metadata: dict