from pydantic import BaseModel, ConfigDict


class UserSettingsUpdate(BaseModel):
    theme: str
    ai_provider: str
    default_model: str
    language: str
    voice_enabled: bool


class UserSettingsResponse(UserSettingsUpdate):
    model_config = ConfigDict(
        from_attributes=True
    )