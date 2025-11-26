# app/core/config.py
"""
Configuration module.
- Loads environment variables from .env file
- Provides type-safe configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    mongodb_url: str
    mongodb_db_name: str = "fastapi_db"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
