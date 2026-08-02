from agent.conversation.models import ConversationContext
from agent.memory.short_term.models import ShortTermMemory
from agent.memory.short_term.policy import ShortTermMemoryPolicy
from agent.memory.short_term.tokenizer import TokenCounter
from agent.memory.short_term.summarizer import ConversationSummarizer


class ShortTermMemoryManager:
    """
    Builds an optimized conversation window for the LLM.
    """

    def __init__(
        self,
        policy: ShortTermMemoryPolicy | None = None,
        summarizer: ConversationSummarizer | None = None,
    ):
        self._policy = policy or ShortTermMemoryPolicy()
        self._summarizer = summarizer

    async def build(
        self,
        conversation: ConversationContext,
    ) -> ShortTermMemory:
        budget = (
            self._policy.max_input_tokens
            - self._policy.reserved_response_tokens
        )

        selected = []
        used_tokens = 0

        for message in reversed(conversation.messages):
            tokens = TokenCounter.count_message(message)

            if used_tokens + tokens > budget:
                break

            selected.append(message)
            used_tokens += tokens

        selected.reverse()

        if len(selected) < self._policy.minimum_messages:
            selected = conversation.messages[-self._policy.minimum_messages :]

        overflow = conversation.messages[: len(conversation.messages) - len(selected)]
        summary = None

        if (
            overflow
            and len(overflow) >= self._policy.minimum_messages_before_summary
            and self._policy.enable_summary
            and self._summarizer
        ):
            summary = await self._summarizer.summarize(overflow)

        return ShortTermMemory(
            messages=selected,
            summary=summary,
            token_count=used_tokens,
        )
