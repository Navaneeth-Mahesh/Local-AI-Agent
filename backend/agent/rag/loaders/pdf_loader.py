from pathlib import Path

from pypdf import PdfReader

from agent.rag.loaders.base import (
    BaseDocumentLoader,
)
from agent.rag.models import Document


class PdfLoader(
    BaseDocumentLoader,
):

    def supports(
        self,
        path: Path,
    ) -> bool:

        return path.suffix.lower() == ".pdf"

    def load(
        self,
        path: Path,
    ) -> Document:

        reader = PdfReader(path)

        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        return Document(
            path=path,
            title=path.stem,
            content=text,
            metadata={
                "pages": len(reader.pages),
            },
        )