from agent.conversation.models import ConversationMessage


class TokenCounter:
    """
    Estimates token usage.

    This implementation is intentionally
    approximate.

    Later we'll replace it with the
    provider-specific tokenizer.
    """

    @staticmethod
    def count_text(
        text: str,
    ) -> int:

        return max(
            1,
            len(text.split()),
        )

    @classmethod
    def count_message(
        cls,
        message: ConversationMessage,
    ) -> int:

        return cls.count_text(
            message.content
        )