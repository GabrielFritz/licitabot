from typing import List

from pydantic import BaseModel, Field


class GenerateEmbeddingRequest(BaseModel):
    text: str = Field(..., description="Text to generate embedding for")


class GenerateEmbeddingResponse(BaseModel):
    embedding_vector: List[float] = Field(..., description="Generated embedding vector")
    embedding_dimensions: int = Field(
        ..., description="Number of dimensions in the vector"
    )
    text: str = Field(..., description="Original text that was embedded")


class GenerateEmbeddingsBatchRequest(BaseModel):
    texts: List[str] = Field(
        ..., description="List of texts to generate embeddings for"
    )


class GenerateEmbeddingsBatchResponse(BaseModel):
    embedding_vectors: List[List[float]] = Field(
        ..., description="Generated embedding vectors"
    )
    embedding_dimensions: int = Field(
        ..., description="Number of dimensions in the vectors"
    )
    texts: List[str] = Field(..., description="Original texts that were embedded")
