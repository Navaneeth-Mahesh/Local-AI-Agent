from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

@abstractmethod
async def stream(
    self,
    prompt,
) -> AsyncGenerator[str, None]:
    ...
from .models import (
    LLMRequest,
    LLMResponse,
)


class BaseLLMProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a response from the language model.
        """
        raise NotImplementedError