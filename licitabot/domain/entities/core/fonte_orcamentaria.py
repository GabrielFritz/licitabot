from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class FonteOrcamentaria(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    codigo: PositiveInt
    nome: str
    descricao: str
    data_inclusao: datetime = Field(..., alias="dataInclusao")
