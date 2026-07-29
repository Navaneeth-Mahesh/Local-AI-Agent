from agent.conversation.models import ConversationMessage


class MemoryExtractor:
    """
    Extracts persistent facts from
    conversations.

    LLM-based implementation will
    be added later.
    """

    async def extract(
        self,
        message: ConversationMessage,
    ) -> list[str]:

        return []