from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from typing import List, TYPE_CHECKING

from licitabot.infrastructure.repositories.database_schemas.core.base import Base

if TYPE_CHECKING:
    from licitabot.infrastructure.repositories.database_schemas.core.contratacao import (
        Contratacao,
    )


class FonteOrcamentaria(Base):
    """Fontes orçamentárias."""

    __tablename__ = "fontes_orcamentarias"

    codigo = Column(Integer, unique=True, nullable=False, primary_key=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    data_inclusao = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    contratacoes: Mapped[List["Contratacao"]] = relationship(
        "Contratacao",
        secondary="contratacoes_fontes_orcamentarias",
        back_populates="fontes_orcamentarias",
    )

    def __repr__(self):
        return f"<FonteOrcamentaria(codigo={self.codigo}, nome='{self.nome}')>"
