from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from licitabot.infrastructure.database.base import Base


class RawContratacao(Base):
    __tablename__ = "contratacoes"
    numero_controle_pncp = Column(String, primary_key=True)
    meta = Column(JSONB)

    items = relationship(
        "RawItemContratacao", back_populates="contratacao", cascade="all, delete-orphan"
    )


class RawItemContratacao(Base):
    __tablename__ = "item_contratacoes"
    numero_controle_pncp = Column(
        String, ForeignKey("contratacoes.numero_controle_pncp"), primary_key=True
    )
    numero_item = Column(Integer, primary_key=True)
    meta = Column(JSONB)

    contratacao = relationship("RawContratacao", back_populates="items")
