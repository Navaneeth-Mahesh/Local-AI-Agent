from agent.context.models import LLMContext
from agent.context.providers import BaseContextProvider


class ContextBuilder:

    def __init__(
        self,
        providers: list[BaseContextProvider] | None = None,
    ):
        self._providers = providers or []

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