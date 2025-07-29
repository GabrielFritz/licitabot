from datetime import datetime

from httpx import AsyncClient, HTTPStatusError, Timeout
from licitabot.application.interfaces.pncp_api_client import (
    PNCPApiClientInterface,
)
from licitabot.config import settings
from licitabot.domain.entities import Contratacao, ItemContratacao
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

TIMEOUT = Timeout(settings.HTTP_TIMEOUT)


class PNCPApiClient(PNCPApiClientInterface):

    def __init__(self, modalidade_contratacao: int, page_size: int):
        self.modalidade_contratacao = modalidade_contratacao
        self.page_size = page_size
        self.client = AsyncClient(timeout=TIMEOUT)

    def _parse_numero_controle_pncp(
        self, numero_controle_pncp: str
    ) -> tuple[str, str, str]:
        try:
            parts = numero_controle_pncp.split("-")
            if len(parts) != 3:
                raise ValueError("Invalid numero_controle_pncp format")

            cnpj = parts[0]

            sequencial_ano = parts[2].split("/")
            if len(sequencial_ano) != 2:
                raise ValueError("Invalid numero_controle_pncp format")

            sequencial = str(int(sequencial_ano[0]))
            ano = str(int(sequencial_ano[1]))

            return cnpj, ano, sequencial

        except (IndexError, ValueError) as e:
            raise ValueError("Invalid numero_controle_pncp format") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(HTTPStatusError),
        reraise=True,
    )
    async def _make_request_with_retry(self, url: str, params: dict = None) -> dict:
        r = await self.client.get(url, params=params)
        r.raise_for_status()
        return r.json()

    async def get_total_paginas(self, data_ini: datetime, data_fim: datetime) -> int:
        params = {
            "dataInicial": data_ini.strftime("%Y%m%d"),
            "dataFinal": data_fim.strftime("%Y%m%d"),
            "codigoModalidadeContratacao": self.modalidade_contratacao,
            "pagina": 1,
            "tamanhoPagina": self.page_size,
        }

        response = await self._make_request_with_retry(
            settings.PNCP_API_CONTRATACOES_URL, params
        )

        return response.get("totalPaginas", 0)

    async def get_contratacoes(
        self, data_ini: datetime, data_fim: datetime, pagina: int
    ) -> list[Contratacao]:

        params = {
            "dataInicial": data_ini.strftime("%Y%m%d"),
            "dataFinal": data_fim.strftime("%Y%m%d"),
            "codigoModalidadeContratacao": self.modalidade_contratacao,
            "pagina": pagina,
            "tamanhoPagina": self.page_size,
        }

        response = await self._make_request_with_retry(
            settings.PNCP_API_CONTRATACOES_URL, params
        )

        return [Contratacao(**d) for d in response.get("data", [])]

    async def get_itens_contratacao(
        self, contratacao: Contratacao
    ) -> list[ItemContratacao]:

        cnpj, ano, seq = self._parse_numero_controle_pncp(
            contratacao.numero_controle_pncp
        )
        url = settings.PNCP_API_ITENS_URL.format(cnpj=cnpj, ano=ano, seq=seq)
        response = await self._make_request_with_retry(url)
        if response:
            return [
                ItemContratacao(
                    **i, numero_controle_pncp=contratacao.numero_controle_pncp
                )
                for i in response
            ]
        return []


pncp_api_client = PNCPApiClient(settings.MODALIDADE_CONTRATACAO, settings.PAGE_SIZE)
