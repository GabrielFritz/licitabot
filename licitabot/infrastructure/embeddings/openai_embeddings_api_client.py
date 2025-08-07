from typing import List

from openai import AsyncOpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from licitabot.application.interfaces.embeddings import (
    EmbeddingApiClientInterface,
)
from licitabot.config import settings


class OpenAIEmbeddingsClient(EmbeddingApiClientInterface):
    """OpenAI-based embeddings client implementation."""

    def __init__(self, api_key: str = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model
        self.client = AsyncOpenAI(api_key=self.api_key)
        self._embedding_dimensions = 1536  # OpenAI text-embedding-ada-002 dimensions

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for a given text."""
        try:
            response = await self.client.embeddings.create(model=self.model, input=text)
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embedding vectors for a batch of texts."""
        try:
            response = await self.client.embeddings.create(
                model=self.model, input=texts
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            raise Exception(f"Failed to generate batch embeddings: {str(e)}")

    def get_embedding_dimensions(self) -> int:
        """Get the number of dimensions for the embedding vectors."""
        return self._embedding_dimensions

    def get_model(self) -> str:
        """Get the model name."""
        return self.model
