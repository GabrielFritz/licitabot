"""
Repositório para operações com órgãos e entidades.
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ingestor.database.models import OrgaoEntidade
from ingestor.models.pncp import OrgaoEntidade as OrgaoEntidadePydantic


class OrgaoRepository:
    """Repositório para operações com órgãos e entidades."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_cnpj(self, cnpj: str) -> Optional[OrgaoEntidade]:
        """
        Busca órgão por CNPJ.

        Args:
            cnpj: CNPJ do órgão

        Returns:
            OrgaoEntidade ou None se não encontrado
        """
        if not cnpj:
            return None

        stmt = select(OrgaoEntidade).where(OrgaoEntidade.cnpj == cnpj)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert(self, orgao_pydantic: OrgaoEntidadePydantic) -> OrgaoEntidade:
        """
        Upsert órgão baseado no CNPJ.

        Args:
            orgao_pydantic: Dados do órgão vindos da API

        Returns:
            OrgaoEntidade salvo/atualizado
        """
        # Busca órgão existente
        orgao_existente = await self.get_by_cnpj(orgao_pydantic.cnpj)

        if orgao_existente:
            # Atualiza dados existentes
            orgao_existente.razao_social = orgao_pydantic.razao_social
            orgao_existente.poder_id = orgao_pydantic.poder_id
            orgao_existente.esfera_id = orgao_pydantic.esfera_id
            return orgao_existente
        else:
            # Cria novo órgão
            orgao_novo = OrgaoEntidade(
                cnpj=orgao_pydantic.cnpj,
                razao_social=orgao_pydantic.razao_social,
                poder_id=orgao_pydantic.poder_id,
                esfera_id=orgao_pydantic.esfera_id,
            )
            self.session.add(orgao_novo)
            return orgao_novo

    async def get_or_create(
        self, orgao_pydantic: OrgaoEntidadePydantic
    ) -> OrgaoEntidade:
        """
        Busca órgão ou cria se não existir.

        Args:
            orgao_pydantic: Dados do órgão vindos da API

        Returns:
            OrgaoEntidade existente ou criado
        """
        return await self.upsert(orgao_pydantic)
