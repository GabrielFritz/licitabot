from typing import Optional, Protocol
from licitabot.domain.entities.core.contratacao import Contratacao
from licitabot.application.dtos import (
    PNCPUpdatedContratacoesParams,
    PNCPUpdatedContratacoesResult,
)


class ContratacoesSourceInterface(Protocol):

    async def get_updated(
        self, params: PNCPUpdatedContratacoesParams
    ) -> PNCPUpdatedContratacoesResult: ...

    async def get(self, numero_controle_pncp: str) -> Optional[Contratacao]: ...
