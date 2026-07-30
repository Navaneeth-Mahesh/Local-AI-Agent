from pathlib import Path

from agent.rag.loaders.base import (
    BaseDocumentLoader,
)
from agent.rag.models import Document


class MarkdownLoader(
    BaseDocumentLoader,
):

    def supports(
        self,
        path: Path,
    ) -> bool:

        return path.suffix.lower() == ".md"

    def load(
        self,
        path: Path,
    ) -> Document:

        content = path.read_text(
            encoding="utf-8",
        )

        return Document(
            path=path,
            title=path.stem,
            content=content,
            metadata={
                "format": "markdown",
            },
        )