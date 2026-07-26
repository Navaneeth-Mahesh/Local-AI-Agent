from agent.conversation.models import (
    ConversationContext,
    ConversationMessage,
)
from app.models.conversation import Conversation


class ConversationMapper:
    """
    Maps ORM models to domain models.
    """

    @staticmethod
    def to_domain(
        conversation: Conversation,
    ) -> ConversationContext:

        return ConversationContext(
            conversation_id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            messages=[
                ConversationMessage(
                    role=message.role,
                    content=message.content,
                    created_at=message.created_at,
                )
                for message in conversation.messages
            ],
        )