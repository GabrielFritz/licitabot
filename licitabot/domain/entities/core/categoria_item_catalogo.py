from datetime import datetime
from pydantic import BaseModel, ConfigDict, PositiveInt, Field


class CategoriaItemCatalogo(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: PositiveInt = Field(..., alias="id")
    nome: str = Field(..., alias="nome")
    descricao: str = Field(..., alias="descricao")
    data_inclusao: datetime = Field(..., alias="dataInclusao")
    data_atualizacao: datetime = Field(..., alias="dataAtualizacao")
    status_ativo: bool = Field(..., alias="statusAtivo")
