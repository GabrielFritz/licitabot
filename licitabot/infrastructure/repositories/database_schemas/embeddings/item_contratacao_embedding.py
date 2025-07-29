from sqlalchemy import Column, String, Integer, Text, Index
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

from licitabot.infrastructure.repositories.database_schemas.core.base import Base

if TYPE_CHECKING:
    from licitabot.infrastructure.repositories.database_schemas.core.item_contratacao import (
        ItemContratacao,
    )


class ItemContratacaoEmbedding(Base):
    """Embeddings for itens de contratação."""

    __tablename__ = "itens_contratacao_embeddings"

    numero_controle_pncp = Column(
        String(100),
        nullable=False,
        primary_key=True,
    )
    numero_item = Column(
        Integer,
        nullable=False,
        primary_key=True,
    )
    embedding_text = Column(Text, nullable=False)
    embedding_vector = Column(Vector(1536), nullable=False)

    # Relationships
    item_contratacao: Mapped["ItemContratacao"] = relationship(
        "ItemContratacao",
        primaryjoin="and_(foreign(ItemContratacaoEmbedding.numero_controle_pncp) == ItemContratacao.numero_controle_pncp, foreign(ItemContratacaoEmbedding.numero_item) == ItemContratacao.numero_item)",
    )

    # Indexes
    __table_args__ = (
        Index(
            "idx_itens_contratacao_embeddings_vector",
            "embedding_vector",
            postgresql_using="ivfflat",
        ),
    )

    def __repr__(self):
        return f"<ItemContratacaoEmbedding(numero_controle_pncp='{self.numero_controle_pncp}', numero_item={self.numero_item})>"
