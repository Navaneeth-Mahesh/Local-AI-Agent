import json
from pathlib import Path

from agent.rag.loaders.base import (
    BaseDocumentLoader,
)
from agent.rag.models import Document


class JsonLoader(
    BaseDocumentLoader,
):

    def supports(
        self,
        path: Path,
    ) -> bool:

        return path.suffix.lower() == ".json"

    def load(
        self,
        path: Path,
    ) -> Document:

        data = json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )

        return Document(
            path=path,
            title=path.stem,
            content=json.dumps(
                data,
                indent=2,
            ),
            metadata={},
        )