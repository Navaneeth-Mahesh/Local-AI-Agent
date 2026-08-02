from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Local AI Agent API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    JWT_SECRET: str = "change-me-super-secret-key-production-ready"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DEBUG: bool = False
    GEMINI_API_KEY: str = ""
    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["*"])

    @property
    def async_database_url(self) -> str:
        url = self.DATABASE_URL
        if url.startswith("sqlite://") and not url.startswith("sqlite+aiosqlite://"):
            return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        if url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
