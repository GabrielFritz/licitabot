# pncp_ingestion_service/ingestor/config.py
"""
Configuration for PNCP ingestion service.

Centralizes all URLs, queue names, and environment variables.
"""

import os
from typing import Final


class Settings:
    """Centralized settings for the PNCP ingestion service."""

    # ───────────────────────────────────────── RabbitMQ Configuration
    RABBITMQ_URL: Final[str] = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")

    # ───────────────────────────────────────── PostgreSQL Configuration
    POSTGRES_HOST: Final[str] = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: Final[str] = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: Final[str] = os.getenv("POSTGRES_DB", "pncp_ingestion")
    POSTGRES_USER: Final[str] = os.getenv("POSTGRES_USER", "pncp_user")
    POSTGRES_PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD", "pncp_pass")

    # Database connection settings
    DB_POOL_SIZE: Final[int] = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW: Final[int] = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    DB_POOL_TIMEOUT: Final[int] = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    DB_POOL_RECYCLE: Final[int] = int(os.getenv("DB_POOL_RECYCLE", "300"))

    # ───────────────────────────────────────── PNCP API Configuration
    # Base URLs for PNCP API endpoints
    PNCP_API_CONTRATACOES_URL: Final[str] = (
        "https://pncp.gov.br/api/consulta/v1/contratacoes/atualizacao"
    )
    PNCP_API_ITENS_URL: Final[str] = (
        "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{seq}/itens"
    )

    # API parameters
    MODALIDADE_CONTRATACAO: Final[int] = 6  # Pregão Eletrônico
    PAGE_SIZE: Final[int] = 50  # tamanhoPagina (API limit)

    # ───────────────────────────────────────── Ingestion Configuration
    ROLLING_WINDOW_MINUTES: Final[int] = int(os.getenv("ROLLING_WINDOW_MINUTES", "15"))

    # HTTP timeout (seconds)
    HTTP_TIMEOUT: Final[float] = float(os.getenv("HTTP_TIMEOUT", "20.0"))

    # ───────────────────────────────────────── Persistence Configuration
    PERSISTENCE_BATCH_SIZE: Final[int] = int(os.getenv("PERSISTENCE_BATCH_SIZE", "100"))
    PERSISTENCE_TIMEOUT: Final[float] = float(os.getenv("PERSISTENCE_TIMEOUT", "30.0"))
    PERSISTENCE_RETRY_ATTEMPTS: Final[int] = int(
        os.getenv("PERSISTENCE_RETRY_ATTEMPTS", "3")
    )

    # ───────────────────────────────────────── Logging Configuration
    LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: Final[str] = os.getenv(
        "LOG_FORMAT", "[%(asctime)s] %(levelname)s: %(message)s"
    )
    SQL_LOGGING: Final[bool] = os.getenv("SQL_LOGGING", "false").lower() == "true"

    # ───────────────────────────────────────── Development Configuration
    DEBUG: Final[bool] = os.getenv("DEBUG", "false").lower() == "true"
    TESTING: Final[bool] = os.getenv("TESTING", "false").lower() == "true"

    INIT_DB: Final[bool] = os.getenv("INIT_DB", "false").lower() == "true"

    # ───────────────────────────────────────── Database URL Generation
    @property
    def database_url(self) -> str:
        """Get database URL from settings."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def async_database_url(self) -> str:
        """Get async database URL from settings."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # ───────────────────────────────────────── Embeddings Configuration
    OPENAI_API_KEY: Final[str] = os.getenv("OPENAI_API_KEY", "")

    LICITABOT_EMBEDDINGS_CLIENT_URL: Final[str] = os.getenv(
        "LICITABOT_EMBEDDINGS_CLIENT_URL",
        "http://embeddings-service-api:8000/embeddings",
    )


# Global settings instance
settings = Settings()
