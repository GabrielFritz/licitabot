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
        "Contratacao", back_populates="orgao_entidade"
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
        "Contratacao", back_populates="unidade_orgao"
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_controle_pncp = Column(String(100), unique=True, nullable=False, index=True)
    srp = Column(Boolean, nullable=False)

    # Foreign Keys
    orgao_entidade_id = Column(
        Integer, ForeignKey("orgaos_entidades.id"), nullable=False
    )
    unidade_orgao_id = Column(Integer, ForeignKey("unidades_orgaos.id"), nullable=False)
    unidade_sub_rogada_id = Column(Integer, ForeignKey("unidades_orgaos.id"))
    orgao_sub_rogado_id = Column(Integer, ForeignKey("orgaos_entidades.id"))
    amparo_legal_id = Column(Integer, ForeignKey("amparos_legais.id"), nullable=False)

    # Datas
    data_inclusao = Column(DateTime, nullable=False)
    data_publicacao_pncp = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)
    data_atualizacao_global = Column(DateTime, nullable=False, index=True)
    data_abertura_proposta = Column(DateTime)
    data_encerramento_proposta = Column(DateTime)

    # Identificação
    ano_compra = Column(Integer, nullable=False)
    sequencial_compra = Column(Integer, nullable=False)
    numero_compra = Column(String(100), nullable=False)
    processo = Column(String(100), nullable=False)

    # Modalidade
    modalidade_id = Column(Integer, nullable=False)
    modalidade_nome = Column(String(100), nullable=False)
    modo_disputa_id = Column(Integer)
    modo_disputa_nome = Column(String(100))

    # Objeto e valores
    objeto_compra = Column(Text, nullable=False)
    valor_total_estimado = Column(DECIMAL(20, 2))
    valor_total_homologado = Column(DECIMAL(20, 2))

    # Campos livres
    informacao_complementar = Column(Text)
    justificativa_presencial = Column(Text)

    # Links
    link_sistema_origem = Column(String(500))
    link_processo_eletronico = Column(String(500))

    # Situação
    situacao_compra_id = Column(String(10), nullable=False)
    situacao_compra_nome = Column(String(100), nullable=False)

    # Instrumento
    tipo_instrumento_convocatorio_codigo = Column(Integer)
    tipo_instrumento_convocatorio_nome = Column(String(100))

    # Usuário
    usuario_nome = Column(String(255), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    orgao_entidade: Mapped["OrgaoEntidade"] = relationship(
        "OrgaoEntidade", back_populates="contratacoes"
    )
    unidade_orgao: Mapped["UnidadeOrgao"] = relationship(
        "UnidadeOrgao", back_populates="contratacoes"
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
    contratacao_id = Column(Integer, ForeignKey("contratacoes.id"), nullable=False)

    numero_item = Column(Integer, nullable=False)
    descricao = Column(Text, nullable=False)
    quantidade = Column(DECIMAL(15, 3), nullable=False)
    unidade_medida = Column(String(50), nullable=False)

    material_ou_servico = Column(String(10), nullable=False)
    material_ou_servico_nome = Column(String(100), nullable=False)

    valor_unitario_estimado = Column(DECIMAL(20, 2))
    valor_total = Column(DECIMAL(20, 2))

    orcamento_sigiloso = Column(Boolean, nullable=False)

    # Categoria e julgamento
    item_categoria_id = Column(Integer, nullable=False)
    item_categoria_nome = Column(String(100), nullable=False)
    criterio_julgamento_id = Column(Integer, nullable=False)
    criterio_julgamento_nome = Column(String(100), nullable=False)
    situacao_compra_item = Column(Integer, nullable=False)
    situacao_compra_item_nome = Column(String(100), nullable=False)

    # Benefício
    tipo_beneficio = Column(Integer, nullable=False)
    tipo_beneficio_nome = Column(String(100), nullable=False)
    incentivo_produtivo_basico = Column(Boolean, nullable=False)

    # Datas
    data_inclusao = Column(DateTime, nullable=False)
    data_atualizacao = Column(DateTime, nullable=False)

    tem_resultado = Column(Boolean, nullable=False)

    # Margem de preferência
    aplicabilidade_margem_preferencia_normal = Column(Boolean, nullable=False)
    aplicabilidade_margem_preferencia_adicional = Column(Boolean, nullable=False)
    percentual_margem_preferencia_normal = Column(DECIMAL(5, 2))
    percentual_margem_preferencia_adicional = Column(DECIMAL(5, 2))

    # Catálogo/NCM
    ncm_nbs_codigo = Column(String(20))
    ncm_nbs_descricao = Column(String(500))
    catalogo = Column(String(100))
    categoria_item_catalogo = Column(String(100))
    catalogo_codigo_item = Column(String(100))

    # Complementos
    informacao_complementar = Column(Text)
    tipo_margem_preferencia = Column(String(100))
    exigencia_conteudo_nacional = Column(Boolean, nullable=False)

    # Outros
    patrimonio = Column(String(100))
    codigo_registro_imobiliario = Column(String(100))
    imagem = Column(Integer)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    contratacao: Mapped["Contratacao"] = relationship(
        "Contratacao", back_populates="itens"
    )

    # Indexes
    __table_args__ = (
        Index("idx_itens_contratacao_id", "contratacao_id"),
        Index("idx_itens_numero_item", "numero_item"),
        Index("idx_itens_categoria", "item_categoria_id"),
    )

    def __repr__(self):
        return f"<ItemContratacao(contratacao_id={self.contratacao_id}, numero_item={self.numero_item})>"


class ContratacaoFonteOrcamentaria(Base):
    """Tabela de relacionamento N:N entre contratações e fontes orçamentárias."""

    __tablename__ = "contratacoes_fontes_orcamentarias"

    contratacao_id = Column(Integer, ForeignKey("contratacoes.id"), primary_key=True)
    fonte_orcamentaria_id = Column(
        Integer, ForeignKey("fontes_orcamentarias.id"), primary_key=True
    )

    def __repr__(self):
        return f"<ContratacaoFonteOrcamentaria(contratacao_id={self.contratacao_id}, fonte_id={self.fonte_orcamentaria_id})>"
