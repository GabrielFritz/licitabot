"""
Repositório para operações com unidades de órgãos.
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ingestor.database.models import UnidadeOrgao
from ingestor.models.pncp import UnidadeOrgao as UnidadeOrgaoPydantic


class UnidadeRepository:
    """Repositório para operações com unidades de órgãos."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_codigo(self, codigo_unidade: str) -> Optional[UnidadeOrgao]:
        """
        Busca unidade por código.

        Args:
            codigo_unidade: Código da unidade

        Returns:
            UnidadeOrgao ou None se não encontrado
        """
        if not codigo_unidade:
            return None

        stmt = select(UnidadeOrgao).where(UnidadeOrgao.codigo_unidade == codigo_unidade)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert(self, unidade_pydantic: UnidadeOrgaoPydantic) -> UnidadeOrgao:
        """
        Upsert unidade baseado no código.

        Args:
            unidade_pydantic: Dados da unidade vindos da API

        Returns:
            UnidadeOrgao salvo/atualizado
        """
        # Busca unidade existente
        unidade_existente = await self.get_by_codigo(unidade_pydantic.codigo_unidade)

        if unidade_existente:
            # Atualiza dados existentes
            unidade_existente.nome_unidade = unidade_pydantic.nome_unidade
            unidade_existente.uf_sigla = unidade_pydantic.uf_sigla.upper()
            unidade_existente.municipio_nome = unidade_pydantic.municipio_nome
            unidade_existente.uf_nome = (
                unidade_pydantic.uf_nome if unidade_pydantic.uf_nome else None
            )
            unidade_existente.codigo_ibge = unidade_pydantic.codigo_ibge
            return unidade_existente
        else:
            # Cria nova unidade
            unidade_nova = UnidadeOrgao(
                codigo_unidade=unidade_pydantic.codigo_unidade,
                nome_unidade=unidade_pydantic.nome_unidade,
                uf_sigla=unidade_pydantic.uf_sigla.upper(),
                municipio_nome=unidade_pydantic.municipio_nome,
                uf_nome=(
                    unidade_pydantic.uf_nome if unidade_pydantic.uf_nome else None
                ),
                codigo_ibge=unidade_pydantic.codigo_ibge,
            )
            self.session.add(unidade_nova)
            return unidade_nova

    async def get_or_create(
        self, unidade_pydantic: UnidadeOrgaoPydantic
    ) -> UnidadeOrgao:
        """
        Busca unidade ou cria se não existir.

        Args:
            unidade_pydantic: Dados da unidade vindos da API

        Returns:
            UnidadeOrgao existente ou criado
        """
        return await self.upsert(unidade_pydantic)
