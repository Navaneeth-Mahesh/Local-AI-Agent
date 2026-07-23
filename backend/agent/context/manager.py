from agent.context.builder import ContextBuilder


class ContextManager:
    """
    High-level entry point for context generation.
    """

    def __init__(
        self,
        builder: ContextBuilder,
    ):
        self._builder = builder

    async def create_context(
        self,
        **kwargs,
    ):
        return await self._builder.build(
            **kwargs
        )