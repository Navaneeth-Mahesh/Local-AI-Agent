from pydantic import BaseModel, ConfigDict


class AIProviderCreate(BaseModel):
    provider: str
    api_key: str
    model: str
    temperature: int


class AIProviderResponse(BaseModel):
    provider: str
    model: str
    temperature: int
    enabled: bool

    model_config = ConfigDict(
        from_attributes=True
    )