from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from typing import List, TYPE_CHECKING

from licitabot.infrastructure.repositories.database_schemas.core.base import Base

if TYPE_CHECKING:
    from licitabot.infrastructure.repositories.database_schemas.core.contratacao import (
        Contratacao,
    )


class UnidadeOrgao(Base):
    """Unidades dos órgãos."""

    __tablename__ = "unidades_orgaos"

    codigo_unidade = Column(String(50), nullable=False, primary_key=True)
    nome_unidade = Column(String(255), nullable=False)
    uf_sigla = Column(String(2), nullable=False)
    municipio_nome = Column(String(255), nullable=False)
    uf_nome = Column(String(100))
    codigo_ibge = Column(String(7))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    contratacoes: Mapped[List["Contratacao"]] = relationship(
        "Contratacao",
        back_populates="unidade_orgao",
        foreign_keys="Contratacao.unidade_orgao_codigo_unidade",
    )
    unidades_sub_rogadas: Mapped[List["Contratacao"]] = relationship(
        "Contratacao",
        back_populates="unidade_sub_rogada",
        foreign_keys="Contratacao.unidade_sub_rogada_codigo_unidade",
    )

    def __repr__(self):
        return f"<UnidadeOrgao(codigo='{self.codigo_unidade}', nome='{self.nome_unidade}')>"
