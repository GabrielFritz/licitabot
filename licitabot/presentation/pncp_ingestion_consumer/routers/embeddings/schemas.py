from pydantic import BaseModel, validator
from datetime import datetime


class PNCPEmbeddingsGenerationMessage(BaseModel):
    data_ini: datetime
    data_fim: datetime

    @validator("data_fim")
    def validate_date_order(cls, v, values):
        data_ini = values.get("data_ini")
        if data_ini and v and v <= data_ini:
            raise ValueError("data_fim must be after data_ini")
        return v
