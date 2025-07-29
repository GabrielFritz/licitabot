from datetime import datetime

from pydantic import BaseModel, validator


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
