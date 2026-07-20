from agent.adapters.gemini.provider import GeminiProvider
from agent.llm.enums import ProviderType
from agent.llm.interfaces import BaseLLMProvider


class LLMFactory:
    """
    Responsible for creating LLM providers.

    The rest of the application should never instantiate
    provider implementations directly.
    """

    @staticmethod
    def create(
        provider: ProviderType,
        api_key: str,
    ) -> BaseLLMProvider:

        match provider:

            case ProviderType.GEMINI:
                return GeminiProvider(api_key)

            case ProviderType.OPENAI:
                raise NotImplementedError(
                    "OpenAI provider not implemented."
                )

            case ProviderType.OLLAMA:
                raise NotImplementedError(
                    "Ollama provider not implemented."
                )

        raise ValueError(f"Unsupported provider: {provider}")