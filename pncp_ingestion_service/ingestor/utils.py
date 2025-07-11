# pncp_ingestion_service/ingestor/utils.py
"""
Utility functions for PNCP ingestion service.

Main functions:
• parse_numero_controle: decomposes numeroControlePNCP into components
• date helpers for ISO formatting and validation
"""

import re
from datetime import datetime
from typing import Tuple


def parse_numero_controle(numero_controle: str) -> Tuple[str, str, str]:
    """
    Decompose numeroControlePNCP into cnpj, ano, sequencial.

    Format: "07854402000100-1-000054/2025"
    Returns: ("07854402000100", "2025", "000054")
    """
    # Pattern: CNPJ-1-SEQUENCIAL/ANO
    pattern = r"^(\d{14})-(\d+)-(\d+)/(\d{4})$"
    match = re.match(pattern, numero_controle)

    if not match:
        raise ValueError(f"Invalid numeroControlePNCP format: {numero_controle}")

    cnpj, _, sequencial, ano = match.groups()
    return cnpj, ano, sequencial


def iso_to_ymd(iso_date: str) -> str:
    """
    Convert ISO date (YYYY-MM-DDTHH:MM:SS) to YYYYMMDD format.

    Used for PNCP API endpoints that require AAAAMMDD format.
    """
    dt = datetime.fromisoformat(iso_date)
    return dt.strftime("%Y%m%d")


def validate_iso_date(date_str: str) -> bool:
    """
    Validate if string is in ISO format YYYY-MM-DDTHH:MM:SS.
    """
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False


def format_iso_local(dt: datetime) -> str:
    """
    Format datetime to ISO string without timezone (local time).

    Returns: YYYY-MM-DDTHH:MM:SS
    """
    return dt.replace(microsecond=0).isoformat(timespec="seconds")
