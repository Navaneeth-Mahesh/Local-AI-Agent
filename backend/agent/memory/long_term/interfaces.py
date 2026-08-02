from abc import ABC, abstractmethod
from agent.memory.long_term.models import MemoryFact


class BaseLongTermMemory(ABC):

    @abstractmethod
    async def remember(
        self,
        fact: MemoryFact,
    ) -> None:
        pass

    @abstractmethod
    async def recall(
        self,
        user_id: int,
        query: str,
    ) -> list[MemoryFact]:
        pass
