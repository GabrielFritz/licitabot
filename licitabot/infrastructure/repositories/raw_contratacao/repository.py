from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from licitabot.application.interfaces import RawContratacaoRepositoryInterface
from licitabot.domain.entities import RawContratacao, RawItemContratacao
from licitabot.domain.value_objects import NumeroControlePNCP
from licitabot.infrastructure.repositories.raw_contratacao.models import (
    RawContratacao as RawContratacaoModel,
)
from licitabot.infrastructure.repositories.raw_contratacao.models import (
    RawItemContratacao as RawItemContratacaoModel,
)


class RawContratacaoRepository(RawContratacaoRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(
        self, numero_controle_pncp: NumeroControlePNCP
    ) -> Optional[RawContratacao]:
        result = await self._get_orm(numero_controle_pncp)
        if not result:
            return None
        return self._from_orm(result)

    async def _get_orm(
        self, numero_controle_pncp: NumeroControlePNCP
    ) -> Optional[RawContratacaoModel]:
        result = await self.session.execute(
            select(RawContratacaoModel)
            .options(selectinload(RawContratacaoModel.items))
            .where(RawContratacaoModel.numero_controle_pncp == numero_controle_pncp)
        )
        return result.scalar_one_or_none()

    def _from_orm(self, model: RawContratacaoModel) -> RawContratacao:
        return RawContratacao(
            numero_controle_pncp=model.numero_controle_pncp,
            meta=model.meta,
            items=[self._from_orm_item(item) for item in model.items],
        )

    def _from_orm_item(self, model: RawItemContratacaoModel) -> RawItemContratacao:
        return RawItemContratacao(
            numero_controle_pncp=model.numero_controle_pncp,
            numero_item=model.numero_item,
            meta=model.meta,
        )

    def _to_orm(self, entity: RawContratacao) -> RawContratacaoModel:
        return RawContratacaoModel(
            numero_controle_pncp=entity.numero_controle_pncp,
            meta=entity.meta,
            items=[self._to_orm_item(item) for item in entity.items],
        )

    def _to_orm_item(self, entity: RawItemContratacao) -> RawItemContratacaoModel:
        return RawItemContratacaoModel(
            numero_controle_pncp=entity.numero_controle_pncp,
            numero_item=entity.numero_item,
            meta=entity.meta,
        )

    async def save(self, entity: RawContratacao, force: bool = False) -> None:
        existing_raw_contratacao = await self._get_orm(entity.numero_controle_pncp)

        entity_orm = self._to_orm(entity)

        if existing_raw_contratacao:
            if not force:
                existing_raw_contratacao_updated_date = (
                    existing_raw_contratacao.meta.get("dataAtualizacaoGlobal")
                )
                entity_updated_date = entity.meta.get("dataAtualizacaoGlobal")
                if (
                    existing_raw_contratacao_updated_date
                    and entity_updated_date
                    and existing_raw_contratacao_updated_date >= entity_updated_date
                ):
                    return

            existing_raw_contratacao.meta = entity_orm.meta

            existing_raw_contratacao.items.clear()

            for item_model in entity_orm.items:
                existing_raw_contratacao.items.append(item_model)

        else:
            self.session.add(entity_orm)

    async def delete(self, numero_controle_pncp: NumeroControlePNCP) -> None:
        await self.session.execute(
            delete(RawContratacaoModel).where(
                RawContratacaoModel.numero_controle_pncp == numero_controle_pncp
            )
        )

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()
