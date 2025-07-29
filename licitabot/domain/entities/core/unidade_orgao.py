from pydantic import BaseModel, ConfigDict, Field


class UnidadeOrgao(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    codigo_unidade: str = Field(..., alias="codigoUnidade")
    nome_unidade: str = Field(..., alias="nomeUnidade")
    uf_sigla: str = Field(..., alias="ufSigla")
    municipio_nome: str = Field(..., alias="municipioNome")
    uf_nome: str = Field(..., alias="ufNome")
    codigo_ibge: str = Field(..., alias="codigoIbge")
