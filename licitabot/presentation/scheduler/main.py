import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from licitabot.settings import settings, logger
from faststream.rabbit import RabbitBroker
from licitabot.domain.services import time_service, ingestion_window_service

broker = RabbitBroker(settings.RABBITMQ_URL, logger=logger)
scheduler = AsyncIOScheduler()


async def publish_raw_contratacao_ingestion_message():
    """Job function (can be scheduled or triggered manually)."""
    ingestion_window = ingestion_window_service.get_ingestion_window()

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


async def start_app():
    # Start Rabbit connection
    await broker.connect()

    # Schedule job: every day at 01:00 São Paulo time
    scheduler.add_job(
        publish_raw_contratacao_ingestion_message,
        trigger="cron",
        hour=1,
        minute=0,
        timezone=time_service.get_timezone(),
    )

    scheduler.start()
    logger.info("Scheduler started. Waiting for jobs...")

    # Keep app alive forever
    await asyncio.Event().wait()


def main():
    asyncio.run(start_app())


if __name__ == "__main__":
    main()
