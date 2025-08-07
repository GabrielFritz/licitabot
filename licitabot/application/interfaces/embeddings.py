from abc import ABC, abstractmethod
from typing import List

from licitabot.domain.entities import Contratacao, ItemContratacao
from licitabot.domain.entities.embedding import (
    ContratacaoEmbedding,
    ItemContratacaoEmbedding,
)


class EmbeddingApiClientInterface(ABC):
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


class PNCPEmbeddingInterface(EmbeddingApiClientInterface):
    """Interface for PNCPEmbeddingApiClient."""

    @abstractmethod
    async def embed_contratacao(self, contratacao: Contratacao) -> ContratacaoEmbedding:
        """Embed a contratacao."""
        raise NotImplementedError

    @abstractmethod
    async def embed_item_contratacao(
        self, item_contratacao: ItemContratacao
    ) -> ItemContratacaoEmbedding:
        """Embed a item_contratacao."""
        raise NotImplementedError
