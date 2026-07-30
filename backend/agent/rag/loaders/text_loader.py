from pathlib import Path

from agent.rag.loaders.base import (
    BaseDocumentLoader,
)
from agent.rag.models import Document


class TextLoader(
    BaseDocumentLoader,
):

    def supports(
        self,
        path: Path,
    ) -> bool:

        return path.suffix.lower() == ".txt"

    def load(
        self,
        path: Path,
    ) -> Document:

        text = path.read_text(
            encoding="utf-8",
        )

        return Document(
            path=path,
            title=path.name,
            content=text,
            metadata={},
        )