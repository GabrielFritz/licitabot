from licitabot.application.interfaces.repositories import (
    RepositoryInterface,
)
from licitabot.domain.entities import UnidadeOrgao
from licitabot.infrastructure.repositories.database_schemas import (
    UnidadeOrgao as UnidadeOrgaoSchema,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, Optional


class UnidadeOrgaoRepository(RepositoryInterface[UnidadeOrgao]):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: Any) -> Optional[UnidadeOrgao]:
        db_result = await self._get_by_id(entity_id)
        if db_result:
            return UnidadeOrgao.model_validate(db_result)
        return None

    async def delete(self, entity_id: Any) -> bool:
        unidade_schema = await self._get_by_id(entity_id)
        if unidade_schema:
            self.session.delete(unidade_schema)
            await self.session.commit()
            return True
        return False

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[UnidadeOrgao]:
        db_results = await self._list_all(limit, offset)
        return [UnidadeOrgao.model_validate(item) for item in db_results]

    async def count_all(self) -> int:
        query = select(func.count(UnidadeOrgaoSchema.codigo_unidade))
        result = await self.session.execute(query)
        return result.scalar()

    async def upsert(self, entity: UnidadeOrgao) -> UnidadeOrgao:
        db_result = await self._upsert(entity)
        return UnidadeOrgao.model_validate(db_result)

    async def _get_by_id(self, entity_id: Any) -> Optional[UnidadeOrgaoSchema]:
        query = select(UnidadeOrgaoSchema).where(
            UnidadeOrgaoSchema.codigo_unidade == entity_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[UnidadeOrgaoSchema]:
        query = (
            select(UnidadeOrgaoSchema)
            .order_by(UnidadeOrgaoSchema.codigo_unidade)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def _upsert(self, entity: UnidadeOrgao) -> UnidadeOrgaoSchema:
        query = select(UnidadeOrgaoSchema).where(
            UnidadeOrgaoSchema.codigo_unidade == entity.codigo_unidade
        )
        result = await self.session.execute(query)
        unidade_existente = result.scalar_one_or_none()

        if unidade_existente:
            unidade_existente.nome_unidade = entity.nome_unidade
            unidade_existente.uf_sigla = entity.uf_sigla
            unidade_existente.municipio_nome = entity.municipio_nome
            unidade_existente.uf_nome = entity.uf_nome
            unidade_existente.codigo_ibge = entity.codigo_ibge
            entity = unidade_existente
        else:
            entity = UnidadeOrgaoSchema(
                codigo_unidade=entity.codigo_unidade,
                nome_unidade=entity.nome_unidade,
                uf_sigla=entity.uf_sigla,
                municipio_nome=entity.municipio_nome,
                uf_nome=entity.uf_nome,
                codigo_ibge=entity.codigo_ibge,
            )
            self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
