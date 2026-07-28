from agent.context.models import LLMContext
from agent.context.providers import BaseContextProvider
from agent.memory.short_term.manager import (
    ShortTermMemoryManager,
)


class ShortTermMemoryProvider(BaseContextProvider):

    def __init__(
        self,
        manager: ShortTermMemoryManager,
    ):
        self._manager = manager

    async def provide(
        self,
        context: LLMContext,
        *,
        state,
        **kwargs,
    ) -> None:

        if state.conversation is None:
            return

        memory = await self._manager.build(
            state.conversation
        )

        history = []

        for message in memory.messages:
            history.append(
                f"{message.role}: {message.content}"
            )

        context.conversation = "\n".join(history)