from agent.context.models import LLMContext
from agent.context.providers import BaseContextProvider


class ConversationContextProvider(BaseContextProvider):
    """
    Adds the active conversation history
    to the LLM context.
    """

    async def provide(
        self,
        context: LLMContext,
        *,
        state,
        **kwargs,
    ) -> None:

        if state.conversation is None:
            return

        history = []

        for message in state.conversation.messages:
            history.append(
                f"{message.role}: {message.content}"
            )

        history.append(
            f"user: {state.user_input}"
        )

        context.conversation = "\n".join(history)