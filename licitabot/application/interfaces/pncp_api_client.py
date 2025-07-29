# classe abstrata para o cliente da API do PNCP

from abc import ABC, abstractmethod
from datetime import datetime

from licitabot.domain.entities import Contratacao, ItemContratacao


class PNCPApiClientInterface(ABC):

    @abstractmethod
    async def get_total_paginas(self, data_ini: datetime, data_fim: datetime) -> int:
        pass

    @abstractmethod
    async def get_contratacoes(
        self, data_ini: datetime, data_fim: datetime, pagina: int
    ) -> list[Contratacao]:
        pass

    @abstractmethod
    async def get_itens_contratacao(
        self, contratacao: Contratacao
    ) -> list[ItemContratacao]:
        pass
