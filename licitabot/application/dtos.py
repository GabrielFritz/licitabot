from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel, validator
from licitabot.domain.entities.core.contratacao import Contratacao

from licitabot.domain.entities.core.value_objects import (
    ModalidadeId,
    YearMonthDay,
)


class PNCPIngestionRequestDTO(BaseModel):

    data_ini: datetime
    data_fim: datetime

    @validator("data_fim")
    def validate_date_order(cls, v, values):

        data_ini = values.get("data_ini")
        if data_ini and v and v <= data_ini:
            raise ValueError("data_fim must be after data_ini")
        return v


class PNCPIngestionResponseDTO(BaseModel):
    success: bool
    message: str
    contratacoes_processadas: int
    itens_contratacao_processados: int
    erros: list[str]
    tempo_processamento: float


class PNCPEmbeddingsGenerationRequestDTO(BaseModel):
    data_ini: datetime
    data_fim: datetime

    @validator("data_fim")
    def validate_date_order(cls, v, values):
        data_ini = values.get("data_ini")
        if data_ini and v and v <= data_ini:
            raise ValueError("data_fim must be after data_ini")
        return v


class PNCPEmbeddingsGenerationResponseDTO(BaseModel):
    success: bool
    message: str
    embeddings_contratacao_gerados: int
    embeddings_item_contratacao_gerados: int
    erros: list[str]
    tempo_processamento: float


class PNCPUpdatedContratacoesParams(TypedDict):
    dataInicial: YearMonthDay
    dataFinal: YearMonthDay
    codigoModalidadeContratacao: ModalidadeId
    pagina: int
    tamanhoPagina: int


class PNCPUpdatedContratacoesResult(BaseModel):
    contratacoes: list[Contratacao]
    total_paginas: int
    total_contratacoes: int
