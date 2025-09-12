from httpx import AsyncClient
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from licitabot.infrastructure.adapters.dtos import (
    PNCPUpdatedContratacoesParamsDTO,
    PNCPUpdatedContratacoesResultDTO,
)
from licitabot.settings import settings


class PNCPApiConsultaAdapter:

    def __init__(self):
        self.client = AsyncClient(timeout=settings.http.timeout)
        self.PNCP_GET_UPDATED_CONTRATACOES_URL = (
            "https://pncp.gov.br/api/consulta/v1/contratacoes/atualizacao"
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=10, max=60),
        retry=retry_if_exception_type((Exception,)),
        reraise=True,
    )
    async def get_updated_contratacoes(
        self, params: PNCPUpdatedContratacoesParamsDTO
    ) -> PNCPUpdatedContratacoesResultDTO:
        response = await self.client.get(
            self.PNCP_GET_UPDATED_CONTRATACOES_URL,
            params=params.model_dump(),
        )
        response.raise_for_status()
        if response.status_code == 204:
            return PNCPUpdatedContratacoesResultDTO(
                data=[],
                totalPaginas=0,
                totalRegistros=0,
                numeroPagina=0,
                paginasRestantes=0,
                empty=True,
            )
        response = response.json()
        return PNCPUpdatedContratacoesResultDTO.model_validate(response)
