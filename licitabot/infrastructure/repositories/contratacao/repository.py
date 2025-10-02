from licitabot.infrastructure.repositories.raw_contratacao.repository import (
    RawContratacaoRepository,
)
from licitabot.domain.entities import (
    RawItemContratacao,
    ItemContratacao,
    RawContratacao,
    Contratacao,
)
from licitabot.domain.value_objects import NumeroControlePNCP
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession


class ContratacaoReadOnlyRepository:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.raw_contratacao_repository = RawContratacaoRepository(session)

    def _from_raw_item_contratacao(
        self, raw_item_contratacao: RawItemContratacao
    ) -> ItemContratacao:
        return ItemContratacao(
            numero_controle_pncp=raw_item_contratacao.numero_controle_pncp,
            numero_item=raw_item_contratacao.numero_item,
            descricao=raw_item_contratacao.meta.get("descricao"),
        )

    def _from_raw_contratacao(self, raw_contratacao: RawContratacao) -> Contratacao:
        items = [
            self._from_raw_item_contratacao(item) for item in raw_contratacao.items
        ]
        return Contratacao(
            numero_controle_pncp=raw_contratacao.numero_controle_pncp,
            objeto=raw_contratacao.meta.get("objetoCompra"),
            items=items,
        )

    async def get(
        self, numero_controle_pncp: NumeroControlePNCP
    ) -> Optional[Contratacao]:

        raw_contratacao = await self.raw_contratacao_repository.get(
            numero_controle_pncp
        )
        if not raw_contratacao:
            return None

        return self._from_raw_contratacao(raw_contratacao)
