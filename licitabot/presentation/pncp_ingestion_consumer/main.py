from contextlib import asynccontextmanager

from faststream import ContextRepo
from faststream.asgi import AsgiFastStream, make_ping_asgi
from faststream.rabbit import RabbitBroker
from licitabot.common.database_utils import get_sync_engine
from licitabot.config import settings
from licitabot.infrastructure.repositories.database_schemas import Base
from licitabot.presentation.pncp_ingestion_consumer.routers.ingestion.router import (
    router as ingestion_router,
)
from licitabot.presentation.pncp_ingestion_consumer.routers.embeddings.router import (
    router as embeddings_router,
)

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("licitabot")


@asynccontextmanager
async def lifespan(context: ContextRepo):
    logger.info("[*] Initializing database tables...")
    try:
        engine = get_sync_engine()
        Base.metadata.create_all(engine)
        logger.info("[*] Database tables created successfully")
    except Exception as e:
        logger.error(f"[!] Warning: Could not create database tables: {e}")
        raise e
    yield


broker = RabbitBroker(settings.RABBITMQ_URL, logger=logger)
app = AsgiFastStream(
    broker,
    logger=logger,
    asgi_routes=[
        ("/health", make_ping_asgi(broker, timeout=5.0, include_in_schema=False))
    ],
    asyncapi_path="/docs",
    lifespan=lifespan,
)

broker.include_router(ingestion_router)
broker.include_router(embeddings_router)
