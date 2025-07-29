from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from typing import List, TYPE_CHECKING

from licitabot.infrastructure.repositories.database_schemas.core.base import Base

if TYPE_CHECKING:
    from licitabot.infrastructure.repositories.database_schemas.core.contratacao import (
        Contratacao,
    )


class AmparoLegal(Base):
    """Amparo legal das contratações."""

    __tablename__ = "amparos_legais"

    codigo = Column(Integer, unique=True, nullable=False, primary_key=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    contratacoes: Mapped[List["Contratacao"]] = relationship(
        "Contratacao",
        back_populates="amparo_legal",
        foreign_keys="Contratacao.amparo_legal_codigo",
    )

    def __repr__(self):
        return f"<AmparoLegal(codigo={self.codigo}, nome='{self.nome}')>"
