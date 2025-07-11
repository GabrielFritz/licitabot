# pncp_ingestion_service/ingestor/config.py
"""
Configuration for PNCP ingestion service.

Centralizes all URLs, queue names, and environment variables.
"""

import os
from typing import Final

# ───────────────────────────────────────── RabbitMQ Configuration

QUEUE_NAME: Final[str] = os.getenv("QUEUE_NAME", "ingest.pncp")
RABBITMQ_URL: Final[str] = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")

# ───────────────────────────────────────── PNCP API Configuration

# Base URLs for PNCP API endpoints
BASE_CONSULTA_URL: Final[str] = (
    "https://pncp.gov.br/api/consulta/v1/contratacoes/atualizacao"
)
BASE_ITENS_URL: Final[str] = (
    "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{seq}/itens"
)

# API parameters
MODALIDADE_CONTRATACAO: Final[int] = 6  # Pregão Eletrônico
PAGE_SIZE: Final[int] = 50  # tamanhoPagina (API limit)

# ───────────────────────────────────────── Ingestion Configuration

ROLLING_WINDOW_MINUTES: Final[int] = int(os.getenv("ROLLING_WINDOW_MINUTES", "15"))

# HTTP timeout (seconds)
HTTP_TIMEOUT: Final[float] = float(os.getenv("HTTP_TIMEOUT", "20.0"))

# ───────────────────────────────────────── Logging Configuration

LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: Final[str] = os.getenv(
    "LOG_FORMAT", "[%(asctime)s] %(levelname)s: %(message)s"
)

# ───────────────────────────────────────── Development Configuration

DEBUG: Final[bool] = os.getenv("DEBUG", "false").lower() == "true"
