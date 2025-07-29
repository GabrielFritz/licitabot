from enum import Enum


class PNCPIngestionMode(str, Enum):
    """Enumeration for PNCP ingestion modes."""

    UPDATE = "update"
    BACKFILL = "backfill"

    __str__ = lambda self: self.value
