from dataclasses import dataclass

DEFAULT_EMBEDDING_MODEL = "text-embedding-004"


@dataclass(slots=True)
class GeminiConfig:
    model: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_output_tokens: int = 2048
    timeout: float = 60.0
    max_retries: int = 3