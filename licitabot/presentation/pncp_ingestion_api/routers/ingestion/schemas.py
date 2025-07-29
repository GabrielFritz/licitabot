from datetime import datetime
from typing import Optional

from licitabot.common.schemas import PNCPIngestionMode
from pydantic import BaseModel, validator


class PNCPIngestionRequest(BaseModel):
    mode: PNCPIngestionMode
    data_ini: Optional[datetime] = None
    data_fim: Optional[datetime] = None

    @validator("data_ini", "data_fim")
    def validate_backfill_dates(cls, v, values):
        mode = values.get("mode")
        if mode == PNCPIngestionMode.BACKFILL:
            if v is None:
                raise ValueError(
                    f"data_ini and data_fim are required for backfill mode"
                )
        return v

    @validator("data_fim")
    def validate_date_order(cls, v, values):

        data_ini = values.get("data_ini")
        if data_ini and v and v <= data_ini:
            raise ValueError("data_fim must be after data_ini")
        return v


class PNCPIngestionResponse(BaseModel):
    request_id: str
