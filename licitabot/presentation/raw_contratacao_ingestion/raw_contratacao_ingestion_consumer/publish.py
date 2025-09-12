from licitabot.domain.services import ingestion_window_service
from licitabot.settings import logger
from licitabot.presentation.raw_contratacao_ingestion.raw_contratacao_ingestion_consumer.broker import (
    get_broker,
)
from datetime import datetime


async def publish_raw_contratacao_ingestion_message(
    data_inicial: datetime = None, data_final: datetime = None
):
    broker = get_broker()
    await broker.connect()

    try:

        ingestion_window = ingestion_window_service.get_ingestion_window(
            data_inicial, data_final
        )

        await broker.publish(
            {
                "dataInicial": ingestion_window.data_inicial,
                "dataFinal": ingestion_window.data_final,
            },
            "raw_contratacao_ingestion_triggered",
        )
        logger.info(
            f"Published ingestion message: {ingestion_window.data_inicial} → {ingestion_window.data_final}"
        )
    finally:
        await broker.close()
