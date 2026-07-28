from agent.conversation.models import ConversationMessage
from agent.llm.interfaces import BaseLLMService


class ConversationSummarizer:
    """
    Generates summaries for older
    conversation history.
    """

    def __init__(
        self,
        llm: BaseLLMService,
    ):
        self._llm = llm

    async def summarize(
        self,
        messages: list[ConversationMessage],
    ) -> str:

        transcript = "\n".join(
            f"{m.role}: {m.content}"
            for m in messages
        )

        prompt = f"""
Summarize the conversation below.

Requirements:

- Preserve important facts.
- Preserve user preferences.
- Preserve decisions.
- Remove repetition.
- Keep under 300 words.

Conversation:

{transcript}
"""

        response = await self._llm.generate(
            prompt=prompt,
        )

        return response.text