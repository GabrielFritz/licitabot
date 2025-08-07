import logging
import uuid

from fastapi import APIRouter, HTTPException, status
from faststream.rabbit import RabbitBroker
from licitabot.common.schemas import PNCPIngestionMode
from licitabot.config import settings
from licitabot.presentation.pncp_ingestion_api.routers.ingestion.schemas import (
    PNCPIngestionRequest,
    PNCPIngestionResponse,
)

from licitabot.presentation.pncp_ingestion_consumer.routers.ingestion.schemas import (
    PNCPIngestionMessage,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/trigger", response_model=PNCPIngestionResponse)
async def trigger(request: PNCPIngestionRequest) -> PNCPIngestionResponse:

    request_id = str(uuid.uuid4())

    try:
        logger.info(
            f"Received ingestion request: {request_id} - mode={request.mode}"
            + (
                f" - {request.data_ini} → {request.data_fim}"
                if request.mode == PNCPIngestionMode.BACKFILL
                else ""
            )
        )
        async with RabbitBroker(settings.RABBITMQ_URL) as broker:
            await broker.publish(
                PNCPIngestionMessage(
                    mode=request.mode,
                    data_ini=request.data_ini,
                    data_fim=request.data_fim,
                ),
                "pncp_ingestion_triggered",
            )
        return PNCPIngestionResponse(request_id=request_id)

    except Exception as e:
        logger.error(f"Error processing ingestion request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
