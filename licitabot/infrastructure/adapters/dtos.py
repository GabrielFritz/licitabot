from typing import Any, Dict, List
from typing import Optional, Literal
from pydantic import BaseModel, RootModel, conint, ConfigDict, field_validator

from licitabot.domain.value_objects import (
    CNPJ,
    Ano,
    CodigoModalidadeContratacao,
    NumeroPagina,
    Sequencial,
    TamanhoPagina,
    TotalPaginas,
    YearMonthDay,
)

entryDTO = Dict[str, Any]
dataDTO = List[entryDTO]


class PNCPUpdatedContratacoesParamsDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    dataInicial: YearMonthDay
    dataFinal: YearMonthDay
    codigoModalidadeContratacao: CodigoModalidadeContratacao
    pagina: NumeroPagina
    tamanhoPagina: TamanhoPagina

    @field_validator("dataInicial", "dataFinal", mode="before")
    @classmethod
    def validate_year_month_day(cls, v):
        if isinstance(v, str):
            return YearMonthDay(v)
        return v

    @field_validator("codigoModalidadeContratacao", mode="before")
    @classmethod
    def validate_codigo_modalidade_contratacao(cls, v):
        if isinstance(v, int):
            return CodigoModalidadeContratacao(v)
        return v

    @field_validator("pagina", mode="before")
    @classmethod
    def validate_numero_pagina(cls, v):
        if isinstance(v, int):
            return NumeroPagina(v)
        return v

    @field_validator("tamanhoPagina", mode="before")
    @classmethod
    def validate_tamanho_pagina(cls, v):
        if isinstance(v, int):
            return TamanhoPagina(v)
        return v


class PNCPUpdatedContratacoesResultDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: dataDTO
    totalPaginas: TotalPaginas
    totalRegistros: conint(ge=0)
    numeroPagina: NumeroPagina
    paginasRestantes: conint(ge=0)
    empty: bool

    @field_validator("totalPaginas", mode="before")
    @classmethod
    def validate_total_paginas(cls, v):
        if isinstance(v, int):
            return TotalPaginas(v)
        return v

    @field_validator("numeroPagina", mode="before")
    @classmethod
    def validate_numero_pagina(cls, v):
        if isinstance(v, int):
            return NumeroPagina(v)
        return v


class PNCPContratacaoItemsParamsDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cnpj: CNPJ
    ano: Ano
    sequencial: Sequencial

    @field_validator("cnpj", mode="before")
    @classmethod
    def validate_cnpj(cls, v):
        if isinstance(v, str):
            return CNPJ(v)
        return v

    @field_validator("ano", mode="before")
    @classmethod
    def validate_ano(cls, v):
        if isinstance(v, int):
            return Ano(v)
        return v

    @field_validator("sequencial", mode="before")
    @classmethod
    def validate_sequencial(cls, v):
        if isinstance(v, int):
            return Sequencial(v)
        return v


class PNCPContratacaoItemsResultDTO(RootModel[List[entryDTO]]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pass


class LiteLLMEmbeddingsParamsDTO(BaseModel):
    model: str = "text-embedding-3-small"
    input: str
    encoding_format: Optional[Literal["float", "base64"]] = None
    user: Optional[str] = None


class LiteLLMEmbeddingItemDTO(BaseModel):
    object: str = "embedding"
    embedding: List[float]
    index: int


class LiteLLMEmbeddingsResultDTO(BaseModel):
    model: str
    data: List[LiteLLMEmbeddingItemDTO]
    usage: Optional[Dict[str, Any]] = None
