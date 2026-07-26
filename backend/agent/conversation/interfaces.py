from abc import ABC, abstractmethod

from agent.conversation.models import (
    ConversationContext,
)


class BaseConversationManager(ABC):

    @abstractmethod
    async def load(
        self,
        conversation_id: int,
    ) -> ConversationContext:
        ...

    @abstractmethod
    async def append_user_message(
        self,
        conversation_id: int,
        content: str,
    ) -> None:
        ...

    @abstractmethod
    async def append_assistant_message(
        self,
        conversation_id: int,
        content: str,
    ) -> None:
        ...
    @abstractmethod
    async def create(
        self,
        *,
        user_id: int,
        title: str,
    ) -> ConversationContext:
        ... 