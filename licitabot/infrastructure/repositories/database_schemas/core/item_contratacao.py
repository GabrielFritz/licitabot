from typing import TYPE_CHECKING

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
    from licitabot.infrastructure.repositories.database_schemas.core.contratacao import (
        Contratacao,
    )


class ItemContratacao(Base):
    """Itens das contratações."""

    __tablename__ = "itens_contratacao"

    numero_controle_pncp = Column(
        String(100),
        ForeignKey("contratacoes.numero_controle_pncp"),
        nullable=False,
        primary_key=True,
    )

    numero_item = Column(Integer, nullable=True, primary_key=True)
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
