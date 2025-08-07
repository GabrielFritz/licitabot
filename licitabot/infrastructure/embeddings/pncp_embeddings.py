from licitabot.application.interfaces.embeddings import (
    PNCPEmbeddingInterface,
)
from licitabot.infrastructure.embeddings.licitabot_embeddings_api_client import (
    LicitabotEmbeddingsClient,
)
from licitabot.domain.entities import (
    Contratacao,
    ContratacaoEmbedding,
    ItemContratacao,
    ItemContratacaoEmbedding,
)


class PNCPEmbeddings(PNCPEmbeddingInterface, LicitabotEmbeddingsClient):
    """PNCP Embeddings API Client."""

    async def embed_contratacao(self, contratacao: Contratacao) -> ContratacaoEmbedding:

        text = contratacao.objeto_compra
        embedding = await self.generate_embedding(text)
        return ContratacaoEmbedding(
            embedding_text=text,
            embedding_vector=embedding,
            numero_controle_pncp=contratacao.numero_controle_pncp,
        )

    async def embed_item_contratacao(
        self, item_contratacao: ItemContratacao
    ) -> ItemContratacaoEmbedding:

        text = item_contratacao.descricao
        embedding = await self.generate_embedding(text)
        return ItemContratacaoEmbedding(
            embedding_text=text,
            embedding_vector=embedding,
            numero_controle_pncp=item_contratacao.numero_controle_pncp,
            numero_item=item_contratacao.numero_item,
        )
