from licitabot.application.dtos import (
    RawContratacaoIngestionParamsDTO,
    RawContratacaoIngestionResultDTO,
)
from licitabot.application.interfaces import (
    RawContratacaoGatewayInterface,
    RawContratacaoRepositoryInterface,
)
from licitabot.infrastructure.execution_tracker.tracker import track
import logging

logger = logging.getLogger("licitabot")


class RawContratacaoIngestionService:
    def __init__(
        self,
        raw_contratacao_gateway: RawContratacaoGatewayInterface,
        raw_contratacao_repository: RawContratacaoRepositoryInterface,
    ):
        self.raw_contratacao_gateway = raw_contratacao_gateway
        self.raw_contratacao_repository = raw_contratacao_repository

    @track("raw_contratacao_ingestion")
    async def run(
        self, params: RawContratacaoIngestionParamsDTO
    ) -> RawContratacaoIngestionResultDTO:

        n_entries_to_process = (
            await self.raw_contratacao_gateway.fetch_number_of_entries(
                params.dataInicial, params.dataFinal
            )
        )

        logger.info(f"[*] Number of entries to process: {n_entries_to_process}")

        try:
            i = 0
            async for (
                raw_contratacao
            ) in self.raw_contratacao_gateway.fetch_updated_contratacoes(
                params.dataInicial, params.dataFinal
            ):
                i += 1
                logger.info(
                    f"[*] Processing raw contratacao {i}/{n_entries_to_process}"
                )
                await self.raw_contratacao_repository.save(raw_contratacao)
                if i % 100 == 0:
                    await self.raw_contratacao_repository.flush()
            await self.raw_contratacao_repository.commit()
        except Exception as e:
            logger.error(f"[!] Error processing raw contratacao {i}: {e}")
            await self.raw_contratacao_repository.rollback()
            raise e

        return RawContratacaoIngestionResultDTO(
            n_raw_contratacoes_processed=n_entries_to_process,
        )
