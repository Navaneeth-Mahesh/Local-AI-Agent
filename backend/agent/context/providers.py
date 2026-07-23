from abc import ABC, abstractmethod
from agent.context.models import LLMContext

class BaseContextProvider(ABC):
    """
    Base interface for all context providers.
    """

    @abstractmethod
    async def provide(
        self,
        context: LLMContext,
        **kwargs,
    ) -> None:
        """
        Enrich the context.
        """