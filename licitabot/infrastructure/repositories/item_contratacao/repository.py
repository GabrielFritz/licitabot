from licitabot.infrastructure.repositories.contratacao.repository import (
    ContratacaoReadOnlyRepository,
)
from licitabot.domain.entities import ItemContratacao, Contratacao
from licitabot.domain.value_objects import NumeroControlePNCP
from typing import Optional


class ItemContratacaoReadOnlyRepository(ContratacaoReadOnlyRepository):

    async def get(
        self, numero_controle_pncp: NumeroControlePNCP, numero_item: int
    ) -> Optional[ItemContratacao]:
        contratacao = await super().get(numero_controle_pncp)
        if not contratacao:
            return None
        item = self._find_item(contratacao, numero_item)
        if not item:
            return None
        return item

    def _find_item(
        self, contratacao: Contratacao, numero_item: int
    ) -> Optional[ItemContratacao]:
        return next(
            (item for item in contratacao.items if item.numero_item == numero_item),
            None,
        )
