from licitabot.application.interfaces.repositories import (
    RepositoryInterface,
)
from licitabot.domain.entities import AmparoLegal
from licitabot.infrastructure.repositories.database_schemas import (
    AmparoLegal as AmparoLegalSchema,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, Optional


class AmparoLegalRepository(RepositoryInterface[AmparoLegal]):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: Any) -> Optional[AmparoLegal]:
        db_result = await self._get_by_id(entity_id)
        if db_result:
            return AmparoLegal.model_validate(db_result)
        return None

    async def delete(self, entity_id: Any) -> bool:
        amparo_schema = await self._get_by_id(entity_id)
        if amparo_schema:
            self.session.delete(amparo_schema)
            await self.session.commit()
            return True
        return False

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[AmparoLegal]:
        db_results = await self._list_all(limit, offset)
        return [AmparoLegal.model_validate(item) for item in db_results]

    async def count_all(self) -> int:
        query = select(func.count(AmparoLegalSchema.codigo))
        result = await self.session.execute(query)
        return result.scalar()

    async def upsert(self, entity: AmparoLegal) -> AmparoLegal:
        db_result = await self._upsert(entity)
        return AmparoLegal.model_validate(db_result)

    async def _get_by_id(self, entity_id: Any) -> Optional[AmparoLegalSchema]:
        query = select(AmparoLegalSchema).where(AmparoLegalSchema.codigo == entity_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[AmparoLegalSchema]:
        query = (
            select(AmparoLegalSchema)
            .order_by(AmparoLegalSchema.codigo)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def _upsert(self, entity: AmparoLegal) -> AmparoLegalSchema:
        query = select(AmparoLegalSchema).where(
            AmparoLegalSchema.codigo == entity.codigo
        )
        result = await self.session.execute(query)
        amparo_existente = result.scalar_one_or_none()

        if amparo_existente:
            amparo_existente.nome = entity.nome
            amparo_existente.descricao = entity.descricao
            entity = amparo_existente
        else:
            entity = AmparoLegalSchema(
                codigo=entity.codigo,
                nome=entity.nome,
                descricao=entity.descricao,
            )
            self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
