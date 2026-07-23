from agent.context.models import LLMContext
from agent.context.providers import BaseContextProvider


class ContextBuilder:
    """
    Builds the complete context sent to the LLM.
    """

    def __init__(
        self,
        providers: list[BaseContextProvider],
    ):
        self._providers = providers

    async def build(
        self,
        **kwargs,
    ) -> LLMContext:

        context = LLMContext()

        for provider in self._providers:
            await provider.provide(
                context,
                **kwargs,
            )

        return context