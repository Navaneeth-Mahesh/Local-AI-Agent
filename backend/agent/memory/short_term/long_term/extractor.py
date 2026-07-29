from agent.memory.long_term.parser import (
    MemoryParser,
)
from agent.memory.long_term.prompts import (
    MEMORY_EXTRACTION_PROMPT,
)


class MemoryExtractor:

    def __init__(
        self,
        llm,
    ):
        self._llm = llm

    async def extract(
        self,
        message,
    ):

        prompt = (
            MEMORY_EXTRACTION_PROMPT
            + "\n\n"
            + message.content
        )

        response = await self._llm.generate(
            prompt=prompt,
        )

        memories = MemoryParser.parse(
            response.text
        )

        for memory in memories:
            memory.source_message_id = message.id

        return memories