from datetime import datetime
from typing import List
from pydantic import BaseModel

from licitabot.domain.entities.core.value_objects import ModalidadeId


class GetUpdatedContratacoesParams(BaseModel):
    start_date: datetime
    end_date: datetime
    modalidades_contratacao: List[ModalidadeId]
