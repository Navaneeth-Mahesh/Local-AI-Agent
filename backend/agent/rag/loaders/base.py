from abc import ABC, abstractmethod
from pathlib import Path

from agent.rag.models import Document


class BaseDocumentLoader(ABC):

    @abstractmethod
    def supports(
        self,
        path: Path,
    ) -> bool:
        ...

    @abstractmethod
    def load(
        self,
        path: Path,
    ) -> Document:
        ...