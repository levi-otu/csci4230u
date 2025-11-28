"""Application configuration using Pydantic settings."""
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    TEST_DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Shorter lifespan for access tokens
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7     # Long-lived refresh tokens

    # Cookie settings
    COOKIE_SECURE: bool = False  # Set to True in production with HTTPS
    COOKIE_SAMESITE: str = "lax"  # CSRF protection
    COOKIE_DOMAIN: str | None = None  # Set domain if needed

    # Application
    APP_NAME: str = "Public Square API"
    DEBUG: bool = False
    BACKEND_CORS_ORIGINS: List[str] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from environment variable."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
