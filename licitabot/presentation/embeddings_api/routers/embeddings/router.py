import logging

from fastapi import APIRouter, HTTPException, status
from licitabot.application.interfaces.embeddings import (
    EmbeddingApiClientInterface,
)
from licitabot.infrastructure.embeddings import OpenAIEmbeddingsClient
from licitabot.presentation.embeddings_api.routers.embeddings.schemas import (
    GenerateEmbeddingRequest,
    GenerateEmbeddingResponse,
    GenerateEmbeddingsBatchRequest,
    GenerateEmbeddingsBatchResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


def get_embeddings_client() -> EmbeddingApiClientInterface:
    """Get embeddings client instance."""
    return OpenAIEmbeddingsClient()


@router.post("/generate", response_model=GenerateEmbeddingResponse)
async def generate_embedding(
    request: GenerateEmbeddingRequest,
) -> GenerateEmbeddingResponse:
    """Generate embedding for a single text."""
    try:
        client = get_embeddings_client()
        embedding_vector = await client.generate_embedding(request.text)

        return GenerateEmbeddingResponse(
            embedding_vector=embedding_vector,
            embedding_dimensions=client.get_embedding_dimensions(),
            text=request.text,
        )
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate embedding: {str(e)}",
        )


@router.post("/generate/batch", response_model=GenerateEmbeddingsBatchResponse)
async def generate_embeddings_batch(
    request: GenerateEmbeddingsBatchRequest,
) -> GenerateEmbeddingsBatchResponse:
    """Generate embeddings for multiple texts."""
    try:
        client = get_embeddings_client()
        embedding_vectors = await client.generate_embeddings_batch(request.texts)

        return GenerateEmbeddingsBatchResponse(
            embedding_vectors=embedding_vectors,
            embedding_dimensions=client.get_embedding_dimensions(),
            texts=request.texts,
        )
    except Exception as e:
        logger.error(f"Error generating batch embeddings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate batch embeddings: {str(e)}",
        )


@router.get("/info")
async def get_embeddings_info():
    """Get information about the embeddings service."""
    try:
        client = get_embeddings_client()
        return {
            "embedding_dimensions": client.get_embedding_dimensions(),
            "service": "OpenAI Embeddings Service",
            "model": client.get_model(),
        }
    except Exception as e:
        logger.error(f"Error getting embeddings info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get embeddings info: {str(e)}",
        )
