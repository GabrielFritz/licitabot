import asyncio
from typing import AsyncGenerator

from licitabot.domain.entities import RawContratacao, RawItemContratacao
from licitabot.domain.value_objects import (
    CodigoModalidadeContratacao,
    NumeroPagina,
    TamanhoPagina,
    TotalPaginas,
    YearMonthDay,
    NumeroControlePNCP,
)
from licitabot.infrastructure.adapters.dtos import (
    PNCPContratacaoItemsParamsDTO,
    PNCPContratacaoItemsResultDTO,
    PNCPUpdatedContratacoesParamsDTO,
    PNCPUpdatedContratacoesResultDTO,
    entryDTO,
)
from licitabot.infrastructure.adapters.pncp_api_consulta_adapter import (
    PNCPApiConsultaAdapter,
)
from licitabot.infrastructure.adapters.pncp_api_pncp_adapter import (
    PNCPApiPncpAdapter,
)
import logging

logger = logging.getLogger("licitabot")


class RawContratacaoGateway:

    def __init__(
        self,
        pncp_api_consulta_adapter: PNCPApiConsultaAdapter,
        pncp_api_pncp_adapter: PNCPApiPncpAdapter,
        codigo_modalidade_contratacao: CodigoModalidadeContratacao,
        tamanho_pagina: TamanhoPagina = 50,
        n_workers: int = 20,
        max_retries: int = 5,
    ):
        self.pncp_api_consulta_adapter = pncp_api_consulta_adapter
        self.pncp_api_pncp_adapter = pncp_api_pncp_adapter
        self.codigo_modalidade_contratacao = codigo_modalidade_contratacao
        self.tamanho_pagina = tamanho_pagina
        self.n_workers = n_workers
        self.max_retries = max_retries

    async def _get_pagina(
        self,
        dataInicial: YearMonthDay,
        dataFinal: YearMonthDay,
        pagina: NumeroPagina,
    ) -> PNCPUpdatedContratacoesResultDTO:
        params = PNCPUpdatedContratacoesParamsDTO(
            dataInicial=dataInicial,
            dataFinal=dataFinal,
            pagina=pagina,
            tamanhoPagina=self.tamanho_pagina,
            codigoModalidadeContratacao=self.codigo_modalidade_contratacao,
        )
        return await self.pncp_api_consulta_adapter.get_updated_contratacoes(params)

    async def _get_num_paginas(
        self, dataInicial: YearMonthDay, dataFinal: YearMonthDay
    ) -> TotalPaginas:
        result = await self._get_pagina(dataInicial, dataFinal, 1)
        return result.totalPaginas

    async def _get_items(self, entry: entryDTO) -> PNCPContratacaoItemsResultDTO:
        params = PNCPContratacaoItemsParamsDTO(
            cnpj=entry["orgaoEntidade"]["cnpj"],
            ano=entry["anoCompra"],
            sequencial=entry["sequencialCompra"],
        )
        return await self.pncp_api_pncp_adapter.get_contratacao_items(params)

    def _convert_to_raw_item_contratacao(
        self, entry: entryDTO, numero_controle_pncp: NumeroControlePNCP
    ) -> RawItemContratacao:
        return RawItemContratacao(
            numero_controle_pncp=numero_controle_pncp,
            numero_item=entry["numeroItem"],
            meta=entry,
        )

    def _convert_to_raw_contratacao(self, entry: entryDTO):
        numero_controle_pncp = entry["numeroControlePNCP"]
        return RawContratacao(
            numero_controle_pncp=numero_controle_pncp,
            meta=entry,
            items=[
                self._convert_to_raw_item_contratacao(item, numero_controle_pncp)
                for item in entry["items"]
            ],
        )

    async def fetch_number_of_entries(
        self, dataInicial: YearMonthDay, dataFinal: YearMonthDay
    ) -> int:
        result = await self._get_pagina(dataInicial, dataFinal, 1)
        return result.totalRegistros

    async def fetch_updated_contratacoes(
        self, dataInicial: YearMonthDay, dataFinal: YearMonthDay
    ) -> AsyncGenerator[RawContratacao, None]:

        num_paginas = await self._get_num_paginas(dataInicial, dataFinal)

        semaphore = asyncio.Semaphore(self.n_workers)
        cooldown_event = asyncio.Event()

        async def fetch_page_with_semaphore(pagina: NumeroPagina):
            async with semaphore:
                retry_count = 0
                while True:
                    try:
                        if cooldown_event.is_set():
                            await asyncio.sleep(0)
                            await cooldown_event.wait()
                        result = await self._get_pagina(dataInicial, dataFinal, pagina)

                        for entry in result.data:
                            items = await self._get_items(entry)
                            entry["items"] = items.root
                        return result
                    except Exception as e:
                        logger.error(f"[!] Error getting page {pagina}: {e}")
                        if not cooldown_event.is_set():
                            cooldown_event.set()
                            logger.debug(f"[*] Cooldown event set")
                            logger.debug(f"[*] Sleeping for 180 seconds")
                            await asyncio.sleep(180)
                            cooldown_event.clear()
                            logger.debug(f"[*] Cooldown event cleared")
                        else:
                            await cooldown_event.wait()
                    retry_count += 1
                    if retry_count > self.max_retries:
                        raise e
                    continue

        tasks = [
            fetch_page_with_semaphore(pagina) for pagina in range(1, num_paginas + 1)
        ]

        for coroutine in asyncio.as_completed(tasks):
            result = await coroutine
            for entry in result.data:
                contratacao = self._convert_to_raw_contratacao(entry)
                yield contratacao
