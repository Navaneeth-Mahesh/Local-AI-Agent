from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming chat request.
    """

    message: str = Field(
        ...,
        min_length=1,
    )

    conversation_id: int | None = None


class ChatResponse(BaseModel):
    """
    API response.
    """

    conversation_id: int

    response: str