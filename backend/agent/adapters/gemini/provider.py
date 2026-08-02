from collections.abc import AsyncGenerator
from agent.llm.interfaces import BaseLLMProvider
from agent.llm.models import (
    LLMRequest,
    LLMResponse,
)

from .client import GeminiClient
from .config import GeminiConfig
from .mapper import GeminiMapper


class GeminiProvider(BaseLLMProvider):

    def __init__(
        self,
        api_key: str,
        config: GeminiConfig | None = None,
    ):
        self._config = config or GeminiConfig()
        self._client = GeminiClient(api_key)

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        contents = GeminiMapper.to_contents(request.messages)

        # Async generation via Google GenAI SDK
        response = await self._client.client.aio.models.generate_content(
            model=self._config.model,
            contents=contents,
        )

        return GeminiMapper.to_response(response)

    async def stream(
        self,
        prompt: str,
    ) -> AsyncGenerator[str, None]:
        response = await self._client.client.aio.models.generate_content_stream(
            model=self._config.model,
            contents=prompt,
        )

        async for chunk in response:
            if chunk.text:
                yield chunk.text