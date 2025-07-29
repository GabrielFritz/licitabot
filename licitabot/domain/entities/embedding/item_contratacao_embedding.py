from pydantic import BaseModel, ConfigDict

from licitabot.domain.entities.embedding.base_embedding import BaseEmbedding


class ItemContratacaoEmbedding(BaseEmbedding):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    numero_controle_pncp: str
    numero_item: int
