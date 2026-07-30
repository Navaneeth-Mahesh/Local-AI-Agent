from agent.rag.chunking.models import (
    DocumentChunk,
)
from agent.rag.chunking.sentence_splitter import (
    SentenceSplitter,
)
from agent.rag.models import Document


class SemanticChunker:

    def __init__(
        self,
        *,
        max_characters: int = 1000,
        overlap_sentences: int = 1,
    ):
        self._splitter = SentenceSplitter()
        self._max_characters = max_characters
        self._overlap = overlap_sentences

    def chunk(
        self,
        document: Document,
    ) -> list[DocumentChunk]:

        sentences = self._splitter.split(
            document.content,
        )

        chunks = []

        current = []

        current_length = 0

        chunk_index = 0

        for sentence in sentences:

            if (
                current
                and current_length + len(sentence)
                > self._max_characters
            ):

                chunks.append(
                    DocumentChunk(
                        id=0,
                        text="\n".join(current),
                        chunk_index=chunk_index,
                        source=str(document.path),
                        metadata=document.metadata,
                    )
                )

                overlap = (
                    current[-self._overlap:]
                    if self._overlap > 0
                    else []
                )

                current = overlap.copy()

                current_length = sum(
                    len(s)
                    for s in current
                )

                chunk_index += 1

            current.append(sentence)

            current_length += len(sentence)

        if current:

            chunks.append(
                DocumentChunk(
                    id=0,
                    text="\n".join(current),
                    chunk_index=chunk_index,
                    source=str(document.path),
                    metadata=document.metadata,
                )
            )

        return chunks