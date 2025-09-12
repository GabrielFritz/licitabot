from httpx import AsyncClient
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from licitabot.infrastructure.adapters.dtos import (
    PNCPContratacaoItemsParamsDTO,
    PNCPContratacaoItemsResultDTO,
)
from licitabot.settings import settings


class PNCPApiPncpAdapter:

    def __init__(self):
        self.client = AsyncClient(timeout=settings.http.timeout)
        self.PNCP_GET_CONTRATACAO_ITEMS_URL = "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=10, max=60),
        retry=retry_if_exception_type((Exception,)),
        reraise=True,
    )
    async def get_contratacao_items(
        self, params: PNCPContratacaoItemsParamsDTO
    ) -> PNCPContratacaoItemsResultDTO:
        cnpj = params.cnpj
        ano = params.ano
        sequencial = params.sequencial
        url = self.PNCP_GET_CONTRATACAO_ITEMS_URL.format(
            cnpj=cnpj, ano=ano, sequencial=sequencial
        )
        response = await self.client.get(url, params={"tamanhoPagina": 10000})
        response.raise_for_status()
        response = response.json()
        return PNCPContratacaoItemsResultDTO.model_validate(response)
