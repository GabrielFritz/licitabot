from abc import ABC, abstractmethod
from typing import List


class EmbeddingsClientInterface(ABC):
    """Interface for embeddings generation clients."""

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for a given text."""
        raise NotImplementedError

    @abstractmethod
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embedding vectors for a batch of texts."""
        raise NotImplementedError

    @abstractmethod
    def get_embedding_dimensions(self) -> int:
        """Get the number of dimensions for the embedding vectors."""
        raise NotImplementedError
