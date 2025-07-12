"""
SQLAlchemy models for PNCP data ingestion.
Based on the Pydantic models from ingestor.models.pncp
"""

from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    DECIMAL,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class OrgaoEntidade(Base):
    """Órgãos e entidades."""

    __tablename__ = "orgaos_entidades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(14), unique=True, nullable=False, index=True)
    razao_social = Column(String(255), nullable=False)
    poder_id = Column(String(1), nullable=False)
    esfera_id = Column(String(1), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    contratacoes: Mapped[List["Contratacao"]] = relationship(
        "Contratacao",
        back_populates="orgao_entidade",
        foreign_keys="Contratacao.orgao_entidade_id",
    )
    orgaos_sub_rogados: Mapped[List["Contratacao"]] = relationship(
        "Contratacao",
        back_populates="orgao_sub_rogado",
        foreign_keys="Contratacao.orgao_sub_rogado_id",
    )

    def __repr__(self):
        return (
            f"<OrgaoEntidade(cnpj='{self.cnpj}', razao_social='{self.razao_social}')>"
        )


class UnidadeOrgao(Base):
    """Unidades dos órgãos."""

    __tablename__ = "unidades_orgaos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_unidade = Column(String(50), nullable=False)
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
        foreign_keys="Contratacao.unidade_orgao_id",
    )
    unidades_sub_rogadas: Mapped[List["Contratacao"]] = relationship(
        "Contratacao",
        back_populates="unidade_sub_rogada",
        foreign_keys="Contratacao.unidade_sub_rogada_id",
    )

    def __repr__(self):
        return f"<UnidadeOrgao(codigo='{self.codigo_unidade}', nome='{self.nome_unidade}')>"


class AmparoLegal(Base):
    """Amparo legal das contratações."""

    __tablename__ = "amparos_legais"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(Integer, unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    contratacoes: Mapped[List["Contratacao"]] = relationship(
        "Contratacao", back_populates="amparo_legal"
    )

    def __repr__(self):
        return f"<AmparoLegal(codigo={self.codigo}, nome='{self.nome}')>"


class FonteOrcamentaria(Base):
    """Fontes orçamentárias."""

    __tablename__ = "fontes_orcamentarias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(Integer, unique=True, nullable=False)
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


class Contratacao(Base):
    """Contratações principais."""

    __tablename__ = "contratacoes"

    numero_controle_pncp = Column(String(100), primary_key=True)
    srp = Column(Boolean, nullable=True)

    # Foreign Keys
    orgao_entidade_id = Column(
        Integer, ForeignKey("orgaos_entidades.id"), nullable=True
    )
    unidade_orgao_id = Column(Integer, ForeignKey("unidades_orgaos.id"), nullable=True)
    unidade_sub_rogada_id = Column(
        Integer, ForeignKey("unidades_orgaos.id"), nullable=True
    )
    orgao_sub_rogado_id = Column(
        Integer, ForeignKey("orgaos_entidades.id"), nullable=True
    )
    amparo_legal_id = Column(Integer, ForeignKey("amparos_legais.id"), nullable=True)

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
    situacao_compra_id = Column(String(10), nullable=True)
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
        "OrgaoEntidade", back_populates="contratacoes", foreign_keys=[orgao_entidade_id]
    )
    unidade_orgao: Mapped["UnidadeOrgao"] = relationship(
        "UnidadeOrgao", back_populates="contratacoes", foreign_keys=[unidade_orgao_id]
    )
    unidade_sub_rogada: Mapped[Optional["UnidadeOrgao"]] = relationship(
        "UnidadeOrgao", foreign_keys=[unidade_sub_rogada_id]
    )
    orgao_sub_rogado: Mapped[Optional["OrgaoEntidade"]] = relationship(
        "OrgaoEntidade", foreign_keys=[orgao_sub_rogado_id]
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


class ItemContratacao(Base):
    """Itens das contratações."""

    __tablename__ = "itens_contratacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_controle_pncp = Column(
        String(100), ForeignKey("contratacoes.numero_controle_pncp"), nullable=False
    )

    numero_item = Column(Integer, nullable=True)
    descricao = Column(Text, nullable=True)
    quantidade = Column(DECIMAL(15, 3), nullable=True)
    unidade_medida = Column(String(50), nullable=True)

    material_ou_servico = Column(String(10), nullable=True)
    material_ou_servico_nome = Column(String(100), nullable=True)

    valor_unitario_estimado = Column(DECIMAL(20, 2), nullable=True)
    valor_total = Column(DECIMAL(20, 2), nullable=True)

    orcamento_sigiloso = Column(Boolean, nullable=True)

    # Categoria e julgamento
    item_categoria_id = Column(Integer, nullable=True)
    item_categoria_nome = Column(String(100), nullable=True)
    criterio_julgamento_id = Column(Integer, nullable=True)
    criterio_julgamento_nome = Column(String(100), nullable=True)
    situacao_compra_item = Column(Integer, nullable=True)
    situacao_compra_item_nome = Column(String(100), nullable=True)

    # Benefício
    tipo_beneficio = Column(Integer, nullable=True)
    tipo_beneficio_nome = Column(String(100), nullable=True)
    incentivo_produtivo_basico = Column(Boolean, nullable=True)

    # Datas
    data_inclusao = Column(DateTime, nullable=True)
    data_atualizacao = Column(DateTime, nullable=True)

    tem_resultado = Column(Boolean, nullable=True)

    # Margem de preferência
    aplicabilidade_margem_preferencia_normal = Column(Boolean, nullable=True)
    aplicabilidade_margem_preferencia_adicional = Column(Boolean, nullable=True)
    percentual_margem_preferencia_normal = Column(DECIMAL(5, 2), nullable=True)
    percentual_margem_preferencia_adicional = Column(DECIMAL(5, 2), nullable=True)

    # Catálogo/NCM
    ncm_nbs_codigo = Column(String(20), nullable=True)
    ncm_nbs_descricao = Column(String(500), nullable=True)
    catalogo = Column(String(100), nullable=True)
    categoria_item_catalogo = Column(String(100), nullable=True)
    catalogo_codigo_item = Column(String(100), nullable=True)

    # Complementos
    informacao_complementar = Column(Text, nullable=True)
    tipo_margem_preferencia = Column(String(100), nullable=True)
    exigencia_conteudo_nacional = Column(Boolean, nullable=True)

    # Outros
    patrimonio = Column(String(100), nullable=True)
    codigo_registro_imobiliario = Column(String(100), nullable=True)
    imagem = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    contratacao: Mapped["Contratacao"] = relationship(
        "Contratacao", back_populates="itens"
    )

    # Indexes
    __table_args__ = (
        Index("idx_itens_contratacao_id", "numero_controle_pncp"),
        Index("idx_itens_numero_item", "numero_item"),
        Index("idx_itens_categoria", "item_categoria_id"),
    )

    def __repr__(self):
        return f"<ItemContratacao(numero_controle_pncp='{self.numero_controle_pncp}', numero_item={self.numero_item})>"


class ContratacaoFonteOrcamentaria(Base):
    """Tabela de relacionamento N:N entre contratações e fontes orçamentárias."""

    __tablename__ = "contratacoes_fontes_orcamentarias"

    numero_controle_pncp = Column(
        String(100), ForeignKey("contratacoes.numero_controle_pncp"), primary_key=True
    )
    fonte_orcamentaria_id = Column(
        Integer, ForeignKey("fontes_orcamentarias.id"), primary_key=True
    )

    def __repr__(self):
        return f"<ContratacaoFonteOrcamentaria(numero_controle_pncp='{self.numero_controle_pncp}', fonte_id={self.fonte_orcamentaria_id})>"
