import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from licitabot.config import settings
from licitabot.presentation.pncp_ingestion_api.routers.ingestion.router import (
    router as ingestion_router,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="PNCP Ingestion Service API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global para exceções não capturadas."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
        },
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(
    ingestion_router, prefix="/pncp_ingestion_service", tags=["pncp_ingestion_service"]
)
