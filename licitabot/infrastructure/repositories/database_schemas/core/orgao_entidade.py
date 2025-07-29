from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from typing import List, TYPE_CHECKING

from licitabot.infrastructure.repositories.database_schemas.core.base import Base

if TYPE_CHECKING:
    from licitabot.infrastructure.repositories.database_schemas.core.contratacao import (
        Contratacao,
    )


class OrgaoEntidade(Base):
    """Órgãos e entidades."""

    __tablename__ = "orgaos_entidades"

    cnpj = Column(String(14), unique=True, nullable=False, index=True, primary_key=True)
    razao_social = Column(String(255), nullable=False)
    poder_id = Column(String(1), nullable=False)
    esfera_id = Column(String(1), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    contratacoes: Mapped[List["Contratacao"]] = relationship(
        "Contratacao",
        back_populates="orgao_entidade",
        foreign_keys="Contratacao.orgao_entidade_cnpj",
    )
    orgaos_sub_rogados: Mapped[List["Contratacao"]] = relationship(
        "Contratacao",
        back_populates="orgao_sub_rogado",
        foreign_keys="Contratacao.orgao_sub_rogado_cnpj",
    )

    def __repr__(self):
        return (
            f"<OrgaoEntidade(cnpj='{self.cnpj}', razao_social='{self.razao_social}')>"
        )
