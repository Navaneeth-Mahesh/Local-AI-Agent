import json

from agent.memory.long_term.models import MemoryFact


class MemoryParser:

    @staticmethod
    def parse(
        text: str,
    ) -> list[MemoryFact]:

        try:

            data = json.loads(text)

        except json.JSONDecodeError:

            return []

        memories = []

        for item in data:

            memories.append(
                MemoryFact(
                    content=item["content"],
                    importance=item.get(
                        "importance",
                        0.5,
                    ),
                )
            )

        return memories