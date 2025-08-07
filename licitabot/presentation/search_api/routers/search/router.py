import logging

from fastapi import APIRouter, HTTPException, status
from licitabot.presentation.search_api.routers.search.schemas import (
    SearchRequest,
    SearchResponse,
    SearchInputType,
)
from licitabot.application.interfaces.embeddings import EmbeddingApiClientInterface
from licitabot.infrastructure.embeddings import LicitabotEmbeddingsClient

logger = logging.getLogger(__name__)

router = APIRouter()


def get_embeddings_client() -> EmbeddingApiClientInterface:
    """Get the embeddings client."""
    return LicitabotEmbeddingsClient()


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """Search for a text in the database."""
    try:
        input_type = request.input_type
        if input_type == SearchInputType.TEXT:
            embeddings = await get_embeddings_client().generate_embedding(request.input)
        elif input_type == SearchInputType.EMBEDDING:
            embeddings = request.input
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid input type",
            )
        return SearchResponse(results=[])

    except Exception as e:
        logger.error(f"Error searching for text: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
