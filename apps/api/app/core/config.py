"""
Configuration management for TradeComply API.
Reads environment variables and exposes them as Pydantic settings.
"""

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # ==================== Application ====================
    APP_NAME: str = "TradeComply API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"
    DEBUG: bool = False

    # ==================== Database ====================
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/tradecomply"
    DB_ECHO: bool = False  # Set to True to log SQL queries

    # ==================== Security ====================
    SECRET_KEY: str = "dev-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ==================== Redis ====================
    REDIS_URL: str = "redis://localhost:6379/0"

    # ==================== S3 Storage ====================
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "tradecomply-docs"
    S3_USE_SSL: bool = False

    # ==================== AI Providers ====================
    OCR_PROVIDER: Literal["mock", "azure", "aws", "gcp", "openai"] = "mock"
    LLM_PROVIDER: Literal["mock", "azure", "aws", "gcp", "openai"] = "mock"

    # Azure AI Services
    AZURE_OCR_ENDPOINT: str | None = None
    AZURE_OCR_KEY: str | None = None

    # AWS Services
    AWS_REGION: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4"

    # ==================== CORS ====================
    CORS_ORIGINS: list[str] = ["*"]  # Change in production
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # ==================== Logging ====================
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    SENTRY_DSN: str | None = None

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
