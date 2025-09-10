import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from licitabot.settings import settings, logger
from faststream.rabbit import RabbitBroker
from licitabot.domain.value_objects import YearMonthDay

broker = RabbitBroker(settings.RABBITMQ_URL, logger=logger)
scheduler = AsyncIOScheduler()


async def publish_raw_contratacao_ingestion_message():
    """Job function (can be scheduled or triggered manually)."""
    data_final = datetime.now(ZoneInfo("America/Sao_Paulo"))
    data_inicial = data_final - timedelta(
        days=settings.RAW_CONTRATACAO_INGESTION_DEFAULT_DELTA
    )

    data_inicial = YearMonthDay(data_inicial.strftime("%Y%m%d"))
    data_final = YearMonthDay(data_final.strftime("%Y%m%d"))

    await broker.publish(
        {
            "dataInicial": data_inicial,
            "dataFinal": data_final,
        },
        "raw_contratacao_ingestion_triggered",
    )
    logger.info(f"Published ingestion message: {data_inicial} → {data_final}")


async def start_app():
    # Start Rabbit connection
    await broker.connect()

    # Schedule job: every day at 01:00 São Paulo time
    scheduler.add_job(
        publish_raw_contratacao_ingestion_message,
        trigger="cron",
        hour=1,
        minute=0,
        timezone=ZoneInfo("America/Sao_Paulo"),
    )

    scheduler.start()
    logger.info("Scheduler started. Waiting for jobs...")

    # Keep app alive forever
    await asyncio.Event().wait()


def main():
    asyncio.run(start_app())


if __name__ == "__main__":
    main()
