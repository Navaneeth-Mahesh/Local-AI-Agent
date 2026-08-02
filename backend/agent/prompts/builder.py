from typing import Any
from agent.prompts.base import PromptTemplate


class PromptBuilder:
    """
    Builds prompts from reusable templates and context.
    """

    @staticmethod
    def build(
        template: PromptTemplate,
        **kwargs: Any,
    ) -> str:
        return template.content.format(**kwargs)