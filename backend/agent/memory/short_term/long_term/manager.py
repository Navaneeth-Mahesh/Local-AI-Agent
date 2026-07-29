from agent.memory.long_term.interfaces import (
    BaseLongTermMemory,
)
from agent.memory.long_term.models import (
    MemoryFact,
)


class LongTermMemoryManager(BaseLongTermMemory):

    def __init__(
        self,
        repository,
    ):
        self._repository = repository

    async def remember(
        self,
        fact: MemoryFact,
    ) -> None:

        await self._repository.save(
            fact
        )

    async def recall(
        self,
        user_id: int,
        query: str,
    ) -> list[MemoryFact]:

        return await self._repository.search(
            user_id=user_id,
            query=query,
        )