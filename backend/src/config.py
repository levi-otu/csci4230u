"""Application configuration using Pydantic settings."""
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: str | List[str] | None) -> List[str]:
    """Parse CORS origins from environment variable."""
    if v is None or v == "":
        return []
    if isinstance(v, list):
        return v
    if isinstance(v, str):
        # If it's a JSON array string, parse it
        if v.startswith("["):
            import json
            return json.loads(v)
        # Otherwise, treat as comma-separated string
        return [i.strip() for i in v.split(",") if i.strip()]
    return []


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    TEST_DATABASE_URL: str | None = None  # Only required for testing

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
    BACKEND_CORS_ORIGINS: str = ""  # Will be parsed to List[str]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="after")
    @classmethod
    def assemble_cors_origins(cls, v: str) -> List[str]:
        """Parse CORS origins from environment variable."""
        return parse_cors(v)


settings = Settings()
