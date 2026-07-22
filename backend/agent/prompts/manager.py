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

        return PromptBuilder.build(
            DEFAULT_CHAT,
            system_prompt=SYSTEM_PROMPT,
            conversation=conversation,
            user_input=user_input,
        )

    def build_title_prompt(
        self,
        conversation: str,
    ) -> str:

        return PromptBuilder.build(
            TITLE_GENERATION,
            conversation=conversation,
        )