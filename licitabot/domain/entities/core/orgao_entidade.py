from pydantic import BaseModel, ConfigDict, Field


class OrgaoEntidade(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    cnpj: str
    razao_social: str = Field(..., alias="razaoSocial")
    poder_id: str = Field(..., alias="poderId")
    esfera_id: str = Field(..., alias="esferaId")
