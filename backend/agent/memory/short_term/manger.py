from agent.conversation.models import ConversationContext
from agent.memory.short_term.models import (
    ShortTermMemory,
)
from agent.memory.short_term.policy import (
    ShortTermMemoryPolicy,
)


class ShortTermMemoryManager:
    """
    Builds an optimized
    conversation window.
    """

    def __init__(
        self,
        policy: ShortTermMemoryPolicy,
    ):
        self._policy = policy

    async def build(
        self,
        conversation: ConversationContext,
    ) -> ShortTermMemory:

        messages = conversation.messages[
            -self._policy.max_messages :
        ]

        return ShortTermMemory(
            messages=messages,
        )