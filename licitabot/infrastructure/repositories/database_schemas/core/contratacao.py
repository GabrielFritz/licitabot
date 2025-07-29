from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from licitabot.infrastructure.repositories.database_schemas.core.base import Base

if TYPE_CHECKING:
    from licitabot.infrastructure.repositories.database_schemas.core.orgao_entidade import (
        OrgaoEntidade,
    )
    from licitabot.infrastructure.repositories.database_schemas.core.unidade_orgao import (
        UnidadeOrgao,
    )
    from licitabot.infrastructure.repositories.database_schemas.core.amparo_legal import (
        AmparoLegal,
    )
    from licitabot.infrastructure.repositories.database_schemas.core.fonte_orcamentaria import (
        FonteOrcamentaria,
    )
    from licitabot.infrastructure.repositories.database_schemas.core.item_contratacao import (
        ItemContratacao,
    )


class Contratacao(Base):
    """Contratações principais."""

    __tablename__ = "contratacoes"

    numero_controle_pncp = Column(String(100), primary_key=True)
    srp = Column(Boolean, nullable=True)

    # Foreign Keys
    orgao_entidade_cnpj = Column(
        String(14), ForeignKey("orgaos_entidades.cnpj"), nullable=True
    )
    unidade_orgao_codigo_unidade = Column(
        String(50), ForeignKey("unidades_orgaos.codigo_unidade"), nullable=True
    )
    unidade_sub_rogada_codigo_unidade = Column(
        String(50), ForeignKey("unidades_orgaos.codigo_unidade"), nullable=True
    )
    orgao_sub_rogado_cnpj = Column(
        String(14), ForeignKey("orgaos_entidades.cnpj"), nullable=True
    )
    amparo_legal_codigo = Column(
        Integer, ForeignKey("amparos_legais.codigo"), nullable=True
    )

    # Datas
    data_inclusao = Column(DateTime, nullable=True)
    data_publicacao_pncp = Column(DateTime, nullable=True)
    data_atualizacao = Column(DateTime, nullable=True)
    data_atualizacao_global = Column(DateTime, nullable=True, index=True)
    data_abertura_proposta = Column(DateTime, nullable=True)
    data_encerramento_proposta = Column(DateTime, nullable=True)

    # Identificação
    ano_compra = Column(Integer, nullable=True)
    sequencial_compra = Column(Integer, nullable=True)
    numero_compra = Column(String(100), nullable=True)
    processo = Column(String(100), nullable=True)

    # Modalidade
    modalidade_id = Column(Integer, nullable=True)
    modalidade_nome = Column(String(100), nullable=True)
    modo_disputa_id = Column(Integer, nullable=True)
    modo_disputa_nome = Column(String(100), nullable=True)

    # Objeto e valores
    objeto_compra = Column(Text, nullable=True)
    valor_total_estimado = Column(DECIMAL(20, 2), nullable=True)
    valor_total_homologado = Column(DECIMAL(20, 2), nullable=True)

    # Campos livres
    informacao_complementar = Column(Text, nullable=True)
    justificativa_presencial = Column(Text, nullable=True)

    # Links
    link_sistema_origem = Column(String(500), nullable=True)
    link_processo_eletronico = Column(String(500), nullable=True)

    # Situação
    situacao_compra_id = Column(Integer, nullable=True)
    situacao_compra_nome = Column(String(100), nullable=True)

    # Instrumento
    tipo_instrumento_convocatorio_codigo = Column(Integer, nullable=True)
    tipo_instrumento_convocatorio_nome = Column(String(100), nullable=True)

    # Usuário
    usuario_nome = Column(String(255), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    orgao_entidade: Mapped["OrgaoEntidade"] = relationship(
        "OrgaoEntidade",
        back_populates="contratacoes",
        foreign_keys=[orgao_entidade_cnpj],
    )
    unidade_orgao: Mapped["UnidadeOrgao"] = relationship(
        "UnidadeOrgao",
        back_populates="contratacoes",
        foreign_keys=[unidade_orgao_codigo_unidade],
    )
    unidade_sub_rogada: Mapped[Optional["UnidadeOrgao"]] = relationship(
        "UnidadeOrgao", foreign_keys=[unidade_sub_rogada_codigo_unidade]
    )
    orgao_sub_rogado: Mapped[Optional["OrgaoEntidade"]] = relationship(
        "OrgaoEntidade", foreign_keys=[orgao_sub_rogado_cnpj]
    )
    amparo_legal: Mapped["AmparoLegal"] = relationship(
        "AmparoLegal", back_populates="contratacoes"
    )
    fontes_orcamentarias: Mapped[List["FonteOrcamentaria"]] = relationship(
        "FonteOrcamentaria",
        secondary="contratacoes_fontes_orcamentarias",
        back_populates="contratacoes",
    )
    itens: Mapped[List["ItemContratacao"]] = relationship(
        "ItemContratacao", back_populates="contratacao"
    )

    # Indexes
    __table_args__ = (
        Index("idx_contratacoes_ano_sequencial", "ano_compra", "sequencial_compra"),
        Index("idx_contratacoes_data_atualizacao", "data_atualizacao_global"),
        Index("idx_contratacoes_modalidade", "modalidade_id"),
    )

    def __repr__(self):
        return f"<Contratacao(numero_controle='{self.numero_controle_pncp}', ano={self.ano_compra}, sequencial={self.sequencial_compra})>"
