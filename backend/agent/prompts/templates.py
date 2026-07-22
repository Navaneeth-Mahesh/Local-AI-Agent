from agent.prompts.base import PromptTemplate

DEFAULT_CHAT = PromptTemplate(
    name="default_chat",
    content="""
{system_prompt}

Conversation:

{conversation}

User:

{user_input}
""",
)

TITLE_GENERATION = PromptTemplate(
    name="title_generation",
    content="""
Generate a short conversation title.

Conversation:

{conversation}

Rules:

- Maximum 6 words.
- No punctuation.
- Return title only.
""",
)