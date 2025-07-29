from typing import Any, List, Optional, Tuple

from licitabot.application.interfaces.repositories import (
    RepositoryInterface,
)
from licitabot.domain.entities import ItemContratacao
from licitabot.infrastructure.repositories.database_schemas import (
    ItemContratacao as ItemContratacaoSchema,
)
from sqlalchemy import func, select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession


class ItemContratacaoRepository(RepositoryInterface[ItemContratacao]):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: Any) -> Optional[ItemContratacao]:
        db_result = await self._get_by_id(entity_id)
        if db_result:
            return ItemContratacao.model_validate(db_result)
        return None

    async def upsert(self, entity: ItemContratacao) -> ItemContratacao:
        item_schema = await self._upsert(entity)
        return ItemContratacao.model_validate(item_schema)

    async def delete(self, entity_id: Any) -> bool:
        item_schema = await self._get_by_id(entity_id)
        if item_schema:
            self.session.delete(item_schema)
            await self.session.commit()
            return True
        return False

    async def list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[ItemContratacao]:
        db_results = await self._list_all(limit, offset)
        return [ItemContratacao.model_validate(item) for item in db_results]

    async def count_all(self) -> int:
        query = select(
            func.count(
                func.distinct(
                    tuple_(
                        ItemContratacaoSchema.numero_controle_pncp,
                        ItemContratacaoSchema.numero_item,
                    )
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def _get_by_id(self, entity_id: Any) -> Optional[ItemContratacaoSchema]:
        numero_controle_pncp, numero_item = entity_id
        query = select(ItemContratacaoSchema).where(
            ItemContratacaoSchema.numero_controle_pncp == numero_controle_pncp,
            ItemContratacaoSchema.numero_item == numero_item,
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _upsert(self, entity: ItemContratacao) -> ItemContratacaoSchema:
        item_existente_schema = await self._get_by_id(
            (entity.numero_controle_pncp, entity.numero_item)
        )
        dados_item = entity.model_dump()

        if item_existente_schema:
            for key, value in dados_item.items():
                setattr(item_existente_schema, key, value)
            entidade = item_existente_schema
        else:
            entidade = ItemContratacaoSchema(**dados_item)
            self.session.add(entidade)

        await self.session.commit()
        await self.session.refresh(entidade)
        return entidade

    async def _list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[ItemContratacaoSchema]:
        query = select(ItemContratacaoSchema).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
