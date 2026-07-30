from pathlib import Path

from agent.rag.loaders.base import BaseDocumentLoader


class LoaderFactory:

    def __init__(
        self,
        loaders: list[BaseDocumentLoader],
    ):
        self._loaders = loaders

    def get_loader(
        self,
        path: Path,
    ) -> BaseDocumentLoader:

        for loader in self._loaders:

            if loader.supports(path):
                return loader

        raise ValueError(
            f"No loader registered for {path.suffix}"
        )