from http import HTTPStatus
from typing import Optional, TypedDict
from httpx import AsyncClient
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from httpx import HTTPStatusError, ReadTimeout
from licitabot.application.interfaces.contracatoes_source import (
    ContratacoesSourceInterface,
)
from licitabot.domain.entities.core.contratacao import Contratacao, NumeroControlePNCP
from licitabot.config import settings
from licitabot.application.dtos import (
    PNCPUpdatedContratacoesParams,
    PNCPUpdatedContratacoesResult,
)


class PNCPContratacoesSourceAdapter(ContratacoesSourceInterface):

    def __init__(self):
        self.client = AsyncClient(timeout=settings.HTTP_TIMEOUT)
        self.PNCP_GET_CONTRATACAO_URL = "https://pncp.gov.br/api/consulta/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}"
        self.PNCP_GET_CONTRATACOES_BY_UPDATE_DATE_URL = (
            "https://pncp.gov.br/api/consulta/v1/contratacoes/atualizacao"
        )
        self.PNCP_GET_CONTRATACAO_ITEMS_URL = "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens"

    async def get(
        self, numero_controle_pncp: NumeroControlePNCP
    ) -> Optional[Contratacao]:

        contratacao_metadata = await self._get_contratacao_metadata(
            numero_controle_pncp
        )
        if contratacao_metadata:
            contratacao_items = await self._get_contratacao_items(numero_controle_pncp)
            return Contratacao.model_validate(
                {**contratacao_metadata, "items": contratacao_items}
            )
        else:
            return None

    async def get_updated(
        self, params: PNCPUpdatedContratacoesParams
    ) -> PNCPUpdatedContratacoesResult:

        api_params = {
            "dataInicial": params["dataInicial"],
            "dataFinal": params["dataFinal"],
            "codigoModalidadeContratacao": params["codigoModalidadeContratacao"].value,
            "pagina": params["pagina"],
            "tamanhoPagina": params["tamanhoPagina"],
        }
        response = await self._make_request_with_retry(
            self.PNCP_GET_CONTRATACOES_BY_UPDATE_DATE_URL, params=api_params
        )

        data = response.get("data", [])
        if data:
            contratacoes = []
            for contratacao_metadata in data:
                contratacao_items = await self._get_contratacao_items(
                    NumeroControlePNCP(contratacao_metadata["numeroControlePNCP"])
                )
                contratacoes.append(
                    Contratacao.model_validate(
                        {**contratacao_metadata, "items": contratacao_items}
                    )
                )
            return PNCPUpdatedContratacoesResult(
                contratacoes=contratacoes,
                total_paginas=response.get("totalPaginas", 0),
                total_contratacoes=response.get("totalRegistros", 0),
            )
        else:
            return PNCPUpdatedContratacoesResult(
                contratacoes=[], total_paginas=0, total_contratacoes=0
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((HTTPStatusError, ReadTimeout)),
        reraise=True,
    )
    async def _make_request_with_retry(self, url: str, params: dict = None) -> dict:
        r = await self.client.get(url, params=params)
        if r.status_code == HTTPStatus.NOT_FOUND:
            return None
        r.raise_for_status()
        return r.json()

    async def _get_contratacao_metadata(self, numero_controle_pncp: NumeroControlePNCP):
        components = numero_controle_pncp.parse_components()
        url = self.PNCP_GET_CONTRATACAO_URL.format(
            cnpj=components["cnpj"],
            ano=components["ano"],
            sequencial=components["sequencial"],
        )
        response = await self._make_request_with_retry(url)
        return response

    async def _get_contratacao_items(self, numero_controle_pncp: NumeroControlePNCP):
        components = numero_controle_pncp.parse_components()
        url = self.PNCP_GET_CONTRATACAO_ITEMS_URL.format(
            cnpj=components["cnpj"],
            ano=components["ano"],
            sequencial=components["sequencial"],
        )
        response = await self._make_request_with_retry(url)
        if response is None:
            return []
        for item in response:
            item["numeroControlePncp"] = numero_controle_pncp
            item["item_id"] = f"{numero_controle_pncp}-{item['numeroItem']}"
        return response
