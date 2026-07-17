from pydantic import BaseModel, Field

from .enums import MessageRole


class LLMMessage(BaseModel):
    role: MessageRole
    content: str


class LLMUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMRequest(BaseModel):
    messages: list[LLMMessage]

    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    max_tokens: int | None = None

    stream: bool = False


class LLMResponse(BaseModel):
    content: str

    model: str

    usage: LLMUsage