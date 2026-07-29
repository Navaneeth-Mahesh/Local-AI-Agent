from agent.memory.long_term.manager import (
    LongTermMemoryManager,
)


class MemoryRetriever:

    def __init__(
        self,
        manager: LongTermMemoryManager,
    ):
        self._manager = manager

    async def retrieve(
        self,
        *,
        user_id: int,
        query: str,
    ):

        return await self._manager.recall(
            user_id=user_id,
            query=query,
        )