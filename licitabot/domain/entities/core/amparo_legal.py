from pydantic import BaseModel, ConfigDict, PositiveInt


class AmparoLegal(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    codigo: PositiveInt
    nome: str
    descricao: str
