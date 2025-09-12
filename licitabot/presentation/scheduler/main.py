import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from licitabot.settings import logger
from licitabot.domain.services import time_service
from licitabot.presentation.raw_contratacao_ingestion.raw_contratacao_ingestion_consumer.publish import (
    publish_raw_contratacao_ingestion_message,
)

scheduler = AsyncIOScheduler()


async def start_app():

    scheduler.add_job(
        publish_raw_contratacao_ingestion_message,
        trigger="cron",
        hour=23,
        minute=0,
        timezone=time_service.get_timezone(),
    )

    scheduler.start()
    logger.info("Scheduler started. Waiting for jobs...")

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Scheduler stopped")
        scheduler.shutdown()
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
        scheduler.shutdown()


def main():
    asyncio.run(start_app())


if __name__ == "__main__":
    main()
