from licitabot.application.raw_contratacao_ingestion_service import (
    RawContratacaoIngestionService,
)
from licitabot.domain.value_objects import CodigoModalidadeContratacao
from licitabot.infrastructure.adapters.pncp_api_consulta_adapter import (
    PNCPApiConsultaAdapter,
)
from licitabot.infrastructure.adapters.pncp_api_pncp_adapter import (
    PNCPApiPncpAdapter,
)
from licitabot.infrastructure.gateways.raw_contratacao_gateway import (
    RawContratacaoGateway,
)
from licitabot.infrastructure.repositories.raw_contratacao.repository import (
    RawContratacaoRepository,
)


class ServiceFactory:

    @staticmethod
    def create_raw_contratacao_ingestion_service(
        session,
        codigo_modalidade_contratacao: CodigoModalidadeContratacao = CodigoModalidadeContratacao.PREGAO_ELETRONICO,
    ) -> RawContratacaoIngestionService:

        pncp_api_consulta_adapter = PNCPApiConsultaAdapter()
        pncp_api_pncp_adapter = PNCPApiPncpAdapter()

        raw_contratacao_gateway = RawContratacaoGateway(
            pncp_api_consulta_adapter=pncp_api_consulta_adapter,
            pncp_api_pncp_adapter=pncp_api_pncp_adapter,
            codigo_modalidade_contratacao=codigo_modalidade_contratacao,
        )

        raw_contratacao_repository = RawContratacaoRepository(session)

        return RawContratacaoIngestionService(
            raw_contratacao_gateway, raw_contratacao_repository
        )
