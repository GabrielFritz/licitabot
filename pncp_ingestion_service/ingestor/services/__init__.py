"""
Services for PNCP ingestion service.

Modules:
- ingestion: PNCP API ingestion functions
- persistence: Database persistence service
"""

from .ingestion import ingest_window
from .persistence import (
    persist_contratacao_with_items,
    persist_batch,
    format_persistence_log,
    PersistenceResult,
)

__all__ = [
    "ingest_window",
    "persist_contratacao_with_items",
    "persist_batch",
    "format_persistence_log",
    "PersistenceResult",
]
