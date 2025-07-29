from sqlalchemy import Column, String, Integer, ForeignKey

from licitabot.infrastructure.repositories.database_schemas.core.base import Base


class ContratacaoFonteOrcamentaria(Base):
    """Tabela de relacionamento N:N entre contratações e fontes orçamentárias."""

    __tablename__ = "contratacoes_fontes_orcamentarias"

    numero_controle_pncp = Column(
        String(100), ForeignKey("contratacoes.numero_controle_pncp"), primary_key=True
    )
    fonte_orcamentaria_codigo = Column(
        Integer, ForeignKey("fontes_orcamentarias.codigo"), primary_key=True
    )

    def __repr__(self):
        return f"<ContratacaoFonteOrcamentaria(numero_controle_pncp='{self.numero_controle_pncp}', fonte_codigo={self.fonte_orcamentaria_codigo})>"
