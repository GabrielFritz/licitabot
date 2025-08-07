from faststream import Logger
from faststream.rabbit import RabbitRouter
from licitabot.application.dtos import PNCPEmbeddingsGenerationRequestDTO
from licitabot.presentation.pncp_ingestion_consumer.routers.embeddings.schemas import (
    PNCPEmbeddingsGenerationMessage,
)
from licitabot.application.factories.pncp_embeddings import (
    PNCPEmbeddingsGenerationServiceFactory,
)

router = RabbitRouter()


@router.subscriber("pncp_ingestion_completed")
async def handle_pncp_ingestion_completed(
    message: PNCPEmbeddingsGenerationMessage, logger: Logger
):

    try:

        data_ini, data_fim = message.data_ini, message.data_fim

        logger.info(f"[Generating Embeddings] window={data_ini} → {data_fim}")

        pncp_embeddings_generation_request = PNCPEmbeddingsGenerationRequestDTO(
            data_ini=data_ini,
            data_fim=data_fim,
        )

        async with PNCPEmbeddingsGenerationServiceFactory.create() as embeddings_generator:
            await embeddings_generator.run(pncp_embeddings_generation_request)

        logger.info(f"Embeddings generated for {message.data_ini} → {message.data_fim}")

    except Exception as e:
        logger.error(
            f"Error generating embeddings for {message.data_ini} → {message.data_fim}: {e}"
        )
