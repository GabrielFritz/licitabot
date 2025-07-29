from licitabot.application.interfaces.repositories import (
    RepositoryInterface,
)
from licitabot.domain.entities import OrgaoEntidade
from licitabot.infrastructure.repositories.database_schemas import (
    OrgaoEntidade as OrgaoEntidadeSchema,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, Optional


class OrgaoEntidadeRepository(RepositoryInterface[OrgaoEntidade]):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: Any) -> Optional[OrgaoEntidade]:
        db_result = await self._get_by_id(entity_id)
        if db_result:
            return OrgaoEntidade.model_validate(db_result)
        return None

    async def delete(self, entity_id: Any) -> bool:
        orgao_schema = await self._get_by_id(entity_id)
        if orgao_schema:
            self.session.delete(orgao_schema)
            await self.session.commit()
            return True
        return False

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[OrgaoEntidade]:
        db_results = await self._list_all(limit, offset)
        return [OrgaoEntidade.model_validate(item) for item in db_results]

    async def count_all(self) -> int:
        query = select(func.count(OrgaoEntidadeSchema.cnpj))
        result = await self.session.execute(query)
        return result.scalar()

    async def upsert(self, entity: OrgaoEntidade) -> OrgaoEntidade:
        db_result = await self._upsert(entity)
        return OrgaoEntidade.model_validate(db_result)

    async def _get_by_id(self, entity_id: Any) -> Optional[OrgaoEntidadeSchema]:
        query = select(OrgaoEntidadeSchema).where(OrgaoEntidadeSchema.cnpj == entity_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[OrgaoEntidadeSchema]:
        query = (
            select(OrgaoEntidadeSchema)
            .order_by(OrgaoEntidadeSchema.cnpj)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def _upsert(self, entity: OrgaoEntidade) -> OrgaoEntidadeSchema:
        query = select(OrgaoEntidadeSchema).where(
            OrgaoEntidadeSchema.cnpj == entity.cnpj
        )
        result = await self.session.execute(query)
        orgao_existente = result.scalar_one_or_none()

        if orgao_existente:
            orgao_existente.razao_social = entity.razao_social
            orgao_existente.poder_id = entity.poder_id
            orgao_existente.esfera_id = entity.esfera_id
            entity = orgao_existente
        else:
            entity = OrgaoEntidadeSchema(
                cnpj=entity.cnpj,
                razao_social=entity.razao_social,
                poder_id=entity.poder_id,
                esfera_id=entity.esfera_id,
            )
            self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
