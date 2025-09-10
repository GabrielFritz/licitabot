from dataclasses import dataclass
from typing import Any, Dict

from licitabot.domain.value_objects import NumeroControlePNCP


@dataclass
class RawItemContratacao:
    numero_controle_pncp: NumeroControlePNCP
    numero_item: int
    meta: Dict[str, Any]


@dataclass
class RawContratacao:
    numero_controle_pncp: NumeroControlePNCP
    meta: Dict[str, Any]
    items: list[RawItemContratacao]
