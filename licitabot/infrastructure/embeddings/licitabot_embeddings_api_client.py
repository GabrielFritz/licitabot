import httpx
from licitabot.application.interfaces.embeddings import (
    EmbeddingApiClientInterface,
)
from licitabot.config import settings
from typing import List
from urllib.parse import urljoin


class LicitabotEmbeddingsClient(EmbeddingApiClientInterface):
    """Licitabot Embeddings API Client."""

    def __init__(self):
        self.url = settings.LICITABOT_EMBEDDINGS_CLIENT_URL

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        url = urljoin(self.url, "generate")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"text": text})
            response.raise_for_status()
            data = response.json()
            return data["embedding_vector"]

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        url = urljoin(self.url, "generate/batch")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"texts": texts})
            response.raise_for_status()
            data = response.json()
            return data["embedding_vectors"]

    async def get_embedding_dimensions(self) -> int:
        """Get embedding dimensions info."""
        url = urljoin(self.url, "info")
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data["embedding_dimensions"]
