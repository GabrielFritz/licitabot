from licitabot.application.interfaces.repository import RepositoryInterface
from licitabot.domain.entities.core.contratacao import Contratacao
from licitabot.application.interfaces.contracatoes_source import (
    ContratacoesSourceInterface,
)
from licitabot.infrastructure.models.contratacao import (
    Contratacao as ContratacaoSchema,
)
from licitabot.application.dtos import UpdateContratacoesDTO
from licitabot.domain.entities import (
    GetUpdatedContratacoesParams,
)


class ContratacoesIngestionService:
    def __init__(
        self,
        contratacao_repository: RepositoryInterface[Contratacao, ContratacaoSchema],
        contratacao_source: ContratacoesSourceInterface,
    ):
        self.contratacao_repository = contratacao_repository
        self.contratacao_source = contratacao_source

    async def run(self, params: UpdateContratacoesDTO):

        get_updated_params = GetUpdatedContratacoesParams(
            start_date=params.start_date,
            end_date=params.end_date,
            modalidades_contratacao=params.modalidades_contratacao,
        )
        contratacoes = await self.contratacao_source.get_updated(get_updated_params)

        for contratacao in contratacoes:
            await self.contratacao_repository.save(contratacao)
