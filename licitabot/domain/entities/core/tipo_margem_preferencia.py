from pydantic import BaseModel, ConfigDict, PositiveInt, Field


class TipoMargemPreferencia(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    codigo: PositiveInt = Field(..., alias="codigo")
    nome: str = Field(..., alias="nome")
