from faststream import Logger
from faststream.rabbit import RabbitRouter
from licitabot.application.dtos import (
    PNCPIngestionRequestDTO,
    PNCPEmbeddingsGenerationRequestDTO,
)
from licitabot.application.factories.ingestion import PNCPIngestionServiceFactory
from licitabot.common.schemas import PNCPIngestionMode
from licitabot.presentation.pncp_ingestion_consumer.routers.ingestion.schemas import (
    PNCPIngestionMessage,
)

router = RabbitRouter()


@router.subscriber("pncp_ingestion_triggered")
@router.publisher("pncp_ingestion_completed")
async def handle_pncp_ingestion_triggered(
    message: PNCPIngestionMessage, logger: Logger
):

    try:
        if message.mode == PNCPIngestionMode.UPDATE:
            data_ini, data_fim = message.get_update_dates()
        else:
            data_ini = message.data_ini
            data_fim = message.data_fim

        logger.info(
            f"[Ingest from PNCP] mode={message.mode}  window={data_ini} → {data_fim}"
        )

        pncp_ingestion_request = PNCPIngestionRequestDTO(
            data_ini=data_ini,
            data_fim=data_fim,
        )

        async with PNCPIngestionServiceFactory.create() as ingestor:
            await ingestor.run(pncp_ingestion_request)

        logger.info(
            f"[Ingest from PNCP] window={data_ini} → {data_fim} processed successfully [✓]"
        )

        return PNCPEmbeddingsGenerationRequestDTO(
            data_ini=data_ini,
            data_fim=data_fim,
        )

    except Exception as e:
        logger.error(f"[Ingest from PNCP] Error: {e}")
        raise
