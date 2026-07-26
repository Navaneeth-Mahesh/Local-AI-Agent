from agent.conversation.interfaces import (
    BaseConversationManager,
)
from agent.conversation.models import (
    ConversationContext,
)


class ConversationManager(BaseConversationManager):
    """
    Coordinates conversation persistence.

    Repository integration will be added
    in the next lesson.
    """

    async def load(
        self,
        conversation_id: int,
    ) -> ConversationContext:

        raise NotImplementedError

    async def append_user_message(
        self,
        conversation_id: int,
        content: str,
    ) -> None:

        raise NotImplementedError

    async def append_assistant_message(
        self,
        conversation_id: int,
        content: str,
    ) -> None:

        raise NotImplementedError