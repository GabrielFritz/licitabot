from contextlib import asynccontextmanager
from faststream.rabbit import RabbitBroker
from licitabot.settings import settings, logger
from licitabot.application.bootstrap import ApplicationBootstrap
from faststream import ContextRepo
from faststream.asgi import AsgiFastStream, make_ping_asgi
from licitabot.presentation.raw_contratacao_ingestion.raw_contratacao_ingestion_consumer.routers.router import (
    router as raw_contratacao_ingestion_router,
)


@asynccontextmanager
async def lifespan(context: ContextRepo):
    await ApplicationBootstrap.bootstrap()
    yield


broker = RabbitBroker(settings.rabbitmq.amqp_url, logger=logger)
app = AsgiFastStream(
    broker,
    logger=logger,
    asgi_routes=[
        ("/health", make_ping_asgi(broker, timeout=5.0, include_in_schema=False))
    ],
    asyncapi_path="/docs",
    lifespan=lifespan,
)

broker.include_router(raw_contratacao_ingestion_router)


def main():
    import uvicorn

    uvicorn.run(
        "licitabot.presentation.raw_contratacao_ingestion.raw_contratacao_ingestion_consumer.main:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
        reload=True,
    )
