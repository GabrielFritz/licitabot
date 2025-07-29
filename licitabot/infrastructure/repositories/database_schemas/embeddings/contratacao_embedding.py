from sqlalchemy import Column, String, Text, ForeignKey, Index
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

from licitabot.infrastructure.repositories.database_schemas.core.base import Base

if TYPE_CHECKING:
    from licitabot.infrastructure.repositories.database_schemas.core.contratacao import (
        Contratacao,
    )


class ContratacaoEmbedding(Base):
    """Embeddings for contratações."""

    __tablename__ = "contratacoes_embeddings"

    numero_controle_pncp = Column(
        String(100),
        ForeignKey("contratacoes.numero_controle_pncp"),
        nullable=False,
        primary_key=True,
    )
    embedding_text = Column(Text, nullable=False)
    embedding_vector = Column(Vector(1536), nullable=False)

    # Relationships
    contratacao: Mapped["Contratacao"] = relationship("Contratacao")

    # Indexes
    __table_args__ = (
        Index(
            "idx_contratacoes_embeddings_vector",
            "embedding_vector",
            postgresql_using="ivfflat",
        ),
    )

    def __repr__(self):
        return f"<ContratacaoEmbedding(numero_controle_pncp='{self.numero_controle_pncp}')>"
