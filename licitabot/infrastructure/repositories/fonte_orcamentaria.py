from licitabot.application.interfaces.repositories import (
    RepositoryInterface,
)
from licitabot.domain.entities import FonteOrcamentaria
from licitabot.infrastructure.repositories.database_schemas import (
    FonteOrcamentaria as FonteOrcamentariaSchema,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, Optional


class FonteOrcamentariaRepository(RepositoryInterface[FonteOrcamentaria]):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: Any) -> Optional[FonteOrcamentaria]:
        db_result = await self._get_by_id(entity_id)
        if db_result:
            return FonteOrcamentaria.model_validate(db_result)
        return None

    async def delete(self, entity_id: Any) -> bool:
        fonte_schema = await self._get_by_id(entity_id)
        if fonte_schema:
            self.session.delete(fonte_schema)
            await self.session.commit()
            return True
        return False

    async def list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[FonteOrcamentaria]:
        db_results = await self._list_all(limit, offset)
        return [FonteOrcamentaria.model_validate(item) for item in db_results]

    async def count_all(self) -> int:
        query = select(func.count(FonteOrcamentariaSchema.codigo))
        result = await self.session.execute(query)
        return result.scalar()

    async def upsert(self, entity: FonteOrcamentaria) -> FonteOrcamentaria:
        db_result = await self._upsert(entity)
        return FonteOrcamentaria.model_validate(db_result)

    async def _get_by_id(self, entity_id: Any) -> Optional[FonteOrcamentariaSchema]:
        query = select(FonteOrcamentariaSchema).where(
            FonteOrcamentariaSchema.codigo == entity_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[FonteOrcamentariaSchema]:
        query = (
            select(FonteOrcamentariaSchema)
            .order_by(FonteOrcamentariaSchema.codigo)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def _upsert(self, entity: FonteOrcamentaria) -> FonteOrcamentariaSchema:
        query = select(FonteOrcamentariaSchema).where(
            FonteOrcamentariaSchema.codigo == entity.codigo
        )
        result = await self.session.execute(query)
        fonte_existente = result.scalar_one_or_none()

        if fonte_existente:
            fonte_existente.nome = entity.nome
            fonte_existente.descricao = entity.descricao
            fonte_existente.data_inclusao = entity.data_inclusao
            entity = fonte_existente
        else:
            entity = FonteOrcamentariaSchema(
                codigo=entity.codigo,
                nome=entity.nome,
                descricao=entity.descricao,
                data_inclusao=entity.data_inclusao,
            )
            self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
