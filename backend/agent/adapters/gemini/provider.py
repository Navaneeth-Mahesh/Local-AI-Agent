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

        contents = GeminiMapper.to_contents(
            request.messages
        )

        response = self._client.client.models.generate_content(

            model=self._config.model,

            contents=contents,
        )

        return GeminiMapper.to_response(
            response
        )
        async def stream(
            self,
            prompt,
        ):

            response = self._client.models.generate_content_stream(
                model=self._model,
                contents=prompt,
            )

            for chunk in response:

                if chunk.text:

                    yield chunk.text