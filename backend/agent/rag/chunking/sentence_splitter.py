import re

from agent.rag.chunking.interfaces import (
    BaseTextSplitter,
)


class SentenceSplitter(
    BaseTextSplitter,
):

    def split(
        self,
        text: str,
    ) -> list[str]:

        text = text.strip()

        if not text:
            return []

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text,
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]