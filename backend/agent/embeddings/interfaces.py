from abc import ABC, abstractmethod

from agent.embeddings.models import (
    EmbeddingResult,
)


class BaseEmbeddingService(ABC):

    @abstractmethod
    async def embed(
        self,
        text: str,
    ) -> EmbeddingResult:
        """
        Generate an embedding for the given text.
        """
        ...