from dataclasses import dataclass

from agent.conversation.models import ConversationMessage


@dataclass(slots=True)
class ShortTermMemory:
    """
    Optimized conversation window
    passed to the LLM.
    """

    messages: list[ConversationMessage]

    summary: str | None = None