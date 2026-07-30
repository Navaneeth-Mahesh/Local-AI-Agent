from agent.context.models import LLMContext
from agent.context.providers import BaseContextProvider
from agent.memory.long_term.retriever import (
    MemoryRetriever,
)


class LongTermMemoryProvider(
    BaseContextProvider,
):

    def __init__(
        self,
        retriever: MemoryRetriever,
    ):
        self._retriever = retriever

    async def provide(
        self,
        context: LLMContext,
        **kwargs,
    ):

        user = kwargs["user"]
        query = kwargs["user_input"]

        memories = await self._retriever.retrieve(
            user_id=user.id,
            query=query,
        )

        if not memories:
            return

        context.memories = "\n".join(
            f"- {memory.content}"
            for memory in memories
        )