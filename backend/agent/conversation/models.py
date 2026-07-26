from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ConversationMessage:
    """
    Domain representation of a conversation message.
    """

    role: str

    content: str

    created_at: datetime


@dataclass(slots=True)
class ConversationContext:
    """
    Loaded conversation passed into the agent.
    """

    conversation_id: int

    user_id: int

    title: str

    messages: list[ConversationMessage]