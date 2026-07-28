from agent.conversation.models import ConversationContext
from agent.memory.short_term.models import (ShortTermMemory,)
from agent.memory.short_term.policy import (ShortTermMemoryPolicy,)
from agent.memory.short_term.tokenizer import ( TokenCounter,)


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
    conversation,
):

    budget = (
        self._policy.max_input_tokens
        - self._policy.reserved_response_tokens
    )

    selected = []

    used_tokens = 0

    for message in reversed(
        conversation.messages
    ):

        tokens = TokenCounter.count_message(
            message
        )

        if (
            used_tokens + tokens
            > budget
        ):
            break

        selected.append(message)

        used_tokens += tokens

    selected.reverse()

    if (
        len(selected)
        < self._policy.minimum_messages
    ):

        selected = conversation.messages[
            -self._policy.minimum_messages :
        ]

    return ShortTermMemory(
        messages=selected,
    )