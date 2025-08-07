from enum import Enum
from pydantic import BaseModel

from licitabot.domain.entities import Contratacao, ItemContratacao


class EntityType(str, Enum):
    CONTRATACAO = "contratacao"
    ITEM_CONTRATACAO = "item_contratacao"


class SearchResult(BaseModel):
    score: float
    entity_type: EntityType
    entity: Contratacao | ItemContratacao
