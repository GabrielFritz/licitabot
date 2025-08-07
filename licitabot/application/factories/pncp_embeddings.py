from licitabot.common.database_utils import get_async_session
from licitabot.infrastructure.repositories import (
    AmparoLegalRepository,
    ContratacaoRepository,
    FonteOrcamentariaRepository,
    ItemContratacaoRepository,
    ContratacaoEmbeddingRepository,
    ItemContratacaoEmbeddingRepository,
    OrgaoEntidadeRepository,
    UnidadeOrgaoRepository,
)
from licitabot.infrastructure.embeddings import PNCPEmbeddings
from licitabot.application.services.pncp_embeddings import (
    PNCPEmbeddingsGenerationService,
)
from licitabot.config import settings


class PNCPEmbeddingsGenerationServiceFactory:

    @classmethod
    def create(cls):

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

        contratacao_embedding_repository = ContratacaoEmbeddingRepository(
            session=session
        )
        item_contratacao_embedding_repository = ItemContratacaoEmbeddingRepository(
            session=session
        )

        embedding = PNCPEmbeddings()

        return PNCPEmbeddingsGenerationService(
            session=session,
            contratacao_repository=contratacao_repository,
            item_contratacao_repository=item_contratacao_repository,
            contratacao_embedding_repository=contratacao_embedding_repository,
            item_contratacao_embedding_repository=item_contratacao_embedding_repository,
            embedding=embedding,
        )
