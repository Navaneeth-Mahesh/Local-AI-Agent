from abc import ABC, abstractmethod

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