from licitabot.application.services.ingestion import PNCPIngestionService
from licitabot.common.database_utils import get_async_session
from licitabot.config import settings
from licitabot.infrastructure.pncp_api_client import PNCPApiClient
from licitabot.infrastructure.repositories import (
    AmparoLegalRepository,
    ContratacaoRepository,
    FonteOrcamentariaRepository,
    ItemContratacaoRepository,
)
from licitabot.infrastructure.repositories.orgao_entidade import (
    OrgaoEntidadeRepository,
)
from licitabot.infrastructure.repositories.unidade_orgao import (
    UnidadeOrgaoRepository,
)


class PNCPIngestionServiceFactory:

    @classmethod
    def create(cls):

        api_client = PNCPApiClient(
            modalidade_contratacao=settings.MODALIDADE_CONTRATACAO,
            page_size=settings.PAGE_SIZE,
        )

        session = get_async_session()
        amparo_legal_repository = AmparoLegalRepository(session=session)
        fonte_orcamentaria_repository = FonteOrcamentariaRepository(session=session)
        orgao_entidade_repository = OrgaoEntidadeRepository(session=session)
        unidade_orgao_repository = UnidadeOrgaoRepository(session=session)

        contratacao_repository = ContratacaoRepository(
            session=session,
            amparo_legal_repository=amparo_legal_repository,
            fonte_orcamentaria_repository=fonte_orcamentaria_repository,
            orgao_entidade_repository=orgao_entidade_repository,
            unidade_orgao_repository=unidade_orgao_repository,
        )
        item_contratacao_repository = ItemContratacaoRepository(session=session)

        return PNCPIngestionService(
            session=session,
            api_client=api_client,
            contratacao_repository=contratacao_repository,
            item_contratacao_repository=item_contratacao_repository,
        )
