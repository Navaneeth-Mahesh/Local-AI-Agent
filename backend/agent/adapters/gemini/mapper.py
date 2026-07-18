from google.genai import types

from agent.llm.models import (
    LLMMessage,
    LLMResponse,
    LLMUsage,
)


class GeminiMapper:

    @staticmethod
    def to_contents(messages: list[LLMMessage]):

        contents = []

        for message in messages:

            contents.append(
                types.Content(
                    role=message.role.value,
                    parts=[
                        types.Part(
                            text=message.content,
                        )
                    ],
                )
            )

        return contents

    @staticmethod
    def to_response(response):

        usage = LLMUsage(
            prompt_tokens=response.usage_metadata.prompt_token_count,
            completion_tokens=response.usage_metadata.candidates_token_count,
            total_tokens=response.usage_metadata.total_token_count,
        )

        return LLMResponse(
            content=response.text,
            model=response.model_version,
            usage=usage,
        )