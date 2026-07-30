from agent.prompts.base import PromptTemplate


class PromptBuilder:
    """
    Builds prompts from reusable templates.
    """

    @staticmethod
    def build(
        template: PromptTemplate,
        **kwargs,
    ) -> str:

        return template.content.format(**kwargs)
    if context.memories:

        prompt.append(
            f"""
    Relevant User Memories:

    {context.memories}
    """
        )