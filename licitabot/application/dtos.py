from pydantic import BaseModel, ConfigDict, field_validator

from licitabot.domain.value_objects import YearMonthDay


class RawContratacaoIngestionParamsDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    dataInicial: YearMonthDay
    dataFinal: YearMonthDay

    @field_validator("dataInicial", "dataFinal", mode="before")
    @classmethod
    def validate_year_month_day(cls, v):
        if isinstance(v, str):
            return YearMonthDay(v)
        return v


class RawContratacaoIngestionResultDTO(BaseModel):
    n_raw_contratacoes_processed: int
