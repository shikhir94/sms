"""Application configuration from environment variables."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "school-service"
    debug: bool = False

    # Database (matches Spring Boot). Use DATABASE_URL for sync; app converts to async.
    database_url: str = "postgresql://postgres:password@localhost:5432/postgres"
    database_echo: bool = False  # Set True to log SQL

    # Server
    host: str = "0.0.0.0"
    # Default app port; matches your frontend expectation
    port: int = 8080


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
