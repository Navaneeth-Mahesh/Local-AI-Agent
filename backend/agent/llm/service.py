from agent.llm.interfaces import BaseLLMProvider
from agent.llm.models import (
    LLMRequest,
    LLMResponse,
)


class LLMService:
    """
    High-level interface used by the application.

    Future responsibilities:

    • Logging
    • Retries
    • Metrics
    • Cost tracking
    • Prompt templates
    • Streaming
    """

    def __init__(
        self,
        provider: BaseLLMProvider,
    ) -> None:

        self._provider = provider

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        return await self._provider.generate(request)