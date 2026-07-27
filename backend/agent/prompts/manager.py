from agent.prompts.builder import PromptBuilder
from agent.prompts.system import SYSTEM_PROMPT
from agent.prompts.templates import (
    DEFAULT_CHAT,
    TITLE_GENERATION,
)


class PromptManager:
    """
    Central entry point for prompt generation.
    """

    def build_chat_prompt(
    self,
    conversation: str,
    user_input: str,
    ) -> str:

        return f"""
    You are a helpful AI assistant.

    Conversation:

    {conversation}

    Current User Message:

    {user_input}
    """