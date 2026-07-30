from agent.rag.chunking.semantic_chunker import (
    SemanticChunker,
)
from agent.rag.models import Document


class ChunkingService:

    def __init__(
        self,
        chunker: SemanticChunker,
    ):
        self._chunker = chunker

    def chunk(
        self,
        document: Document,
    ):

        return self._chunker.chunk(
            document,
        )