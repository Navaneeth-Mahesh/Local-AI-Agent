from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ShortTermMemoryPolicy:
    """
    Configuration for the STM manager.
    """

    max_messages: int = 6000

    reserved_response_token: int = 1500

    minimum_message: int = 6

    reserve_tokens: int = 4000

    enable_summary: bool = True