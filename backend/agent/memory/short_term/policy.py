from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ShortTermMemoryPolicy:
    """
    Configuration for the STM manager.
    """

    max_messages: int = 20

    reserve_tokens: int = 4000

    enable_summary: bool = True