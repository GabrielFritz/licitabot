import time

from licitabot.application.dtos import (
    PNCPIngestionRequestDTO,
    PNCPIngestionResponseDTO,
)
from licitabot.application.interfaces.pncp_api_client import (
    PNCPApiClientInterface,
)
from licitabot.application.interfaces.repositories import (
    RepositoryInterface,
)
from licitabot.domain.entities import Contratacao, ItemContratacao
from sqlalchemy.ext.asyncio import AsyncSession


class PNCPIngestionService:

    def __init__(
        self,
        session: AsyncSession,
        api_client: PNCPApiClientInterface,
        contratacao_repository: RepositoryInterface[Contratacao],
        item_contratacao_repository: RepositoryInterface[ItemContratacao],
    ):
        self.session = session
        self.api_client = api_client
        self.contratacao_repository = contratacao_repository
        self.item_contratacao_repository = item_contratacao_repository

    def is_before_ingestion_window(
        self, contratacao: Contratacao, ingestion_request: PNCPIngestionRequestDTO
    ) -> bool:
        return contratacao.data_atualizacao_global < ingestion_request.data_ini

    def is_after_ingestion_window(
        self, contratacao: Contratacao, ingestion_request: PNCPIngestionRequestDTO
    ) -> bool:
        return contratacao.data_atualizacao_global > ingestion_request.data_fim

    async def run(
        self, ingestion_request: PNCPIngestionRequestDTO
    ) -> PNCPIngestionResponseDTO:

        start_time = time.time()

        try:

            total_paginas = await self.api_client.get_total_paginas(
                ingestion_request.data_ini,
                ingestion_request.data_fim,
            )

            contratacoes_processadas = 0
            itens_contratacao_processados = 0

            for pagina in range(total_paginas, 0, -1):
                contratacoes = await self.api_client.get_contratacoes(
                    ingestion_request.data_ini, ingestion_request.data_fim, pagina
                )
                for i, contratacao in enumerate(contratacoes[::-1], start=1):
                    if self.is_before_ingestion_window(contratacao, ingestion_request):
                        return PNCPIngestionResponseDTO(
                            success=True,
                            message=f"PNCP ingestion from {ingestion_request.data_ini} to {ingestion_request.data_fim} completed successfully",
                            contratacoes_processadas=contratacoes_processadas,
                            itens_contratacao_processados=itens_contratacao_processados,
                            erros=[],
                            tempo_processamento=time.time() - start_time,
                        )
                    if self.is_after_ingestion_window(contratacao, ingestion_request):
                        continue

                    itens_contratacao = await self.api_client.get_itens_contratacao(
                        contratacao
                    )

                    await self.contratacao_repository.upsert(contratacao)
                    for item in itens_contratacao:
                        await self.item_contratacao_repository.upsert(item)

                    contratacoes_processadas += 1
                    itens_contratacao_processados += len(itens_contratacao)

            return PNCPIngestionResponseDTO(
                success=True,
                message=f"PNCP ingestion from {ingestion_request.data_ini} to {ingestion_request.data_fim} completed successfully",
                contratacoes_processadas=contratacoes_processadas,
                itens_contratacao_processados=itens_contratacao_processados,
                erros=[],
                tempo_processamento=time.time() - start_time,
            )
        except Exception as e:
            raise e
            return PNCPIngestionResponseDTO(
                success=False,
                message=f"NCP ingestion from {ingestion_request.data_ini} to {ingestion_request.data_fim} failed",
                contratacoes_processadas=0,
                itens_contratacao_processados=0,
                erros=[str(e)],
                tempo_processamento=time.time() - start_time,
            )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
