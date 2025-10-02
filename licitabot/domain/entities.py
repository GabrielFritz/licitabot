from dataclasses import dataclass, field
from typing import Any, Dict

from licitabot.domain.value_objects import NumeroControlePNCP


@dataclass
class RawItemContratacao:
    numero_controle_pncp: NumeroControlePNCP = field(
        metadata={"description": "Unique PNCP control number for the contract"}
    )
    numero_item: int = field(
        metadata={"description": "Item number within the contract"}
    )
    meta: Dict[str, Any] = field(
        metadata={"description": "Additional metadata for the contract item"}
    )


@dataclass
class RawContratacao:
    numero_controle_pncp: NumeroControlePNCP = field(
        metadata={"description": "Unique PNCP control number for the contract"}
    )
    meta: Dict[str, Any] = field(
        metadata={"description": "Additional metadata for the contract"}
    )
    items: list[RawItemContratacao] = field(
        metadata={"description": "List of items in the contract"}
    )


@dataclass
class ItemContratacao:
    numero_controle_pncp: NumeroControlePNCP = field(
        metadata={"description": "Unique PNCP control number for the contract"}
    )
    numero_item: int = field(
        metadata={"description": "Item number within the contract"}
    )
    descricao: str = field(metadata={"description": "Description of the contract item"})


@dataclass
class Contratacao:
    numero_controle_pncp: NumeroControlePNCP = field(
        metadata={"description": "Unique PNCP control number for the contract"}
    )
    objeto: str = field(metadata={"description": "Object of the contract"})
    items: list[ItemContratacao] = field(
        metadata={"description": "List of items in the contract"}
    )
