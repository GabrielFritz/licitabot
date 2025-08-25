from licitabot.infrastructure.adapter.pncp_contratacoes_source_adapter import (
    PNCPContratacoesSourceAdapter,
)
from licitabot.domain.entities.core.contratacao import NumeroControlePNCP
import asyncio
from licitabot.application.dtos import PNCPUpdatedContratacoesParams
from licitabot.domain.entities.core.value_objects import ModalidadeId
from licitabot.domain.entities.core.value_objects import YearMonthDay
from licitabot.infrastructure.models.amparo_legal import (
    AmparoLegal as AmparoLegalSchema,
)
from licitabot.db import init_db, close_db

from licitabot.infrastructure.repositories.contratacao_repository import (
    ContratacaoRepository,
)


async def test_get_contratacao():
    await init_db()
    try:

        adapter = PNCPContratacoesSourceAdapter()
        contratacao = await adapter.get(
            NumeroControlePNCP("83102277000152-1-000260/2025")
        )

        contratacao_repository = ContratacaoRepository()

        try:
            await contratacao_repository.save(contratacao)
        except Exception as e:
            print(f"Exception during save: {e}")
            import traceback

            traceback.print_exc()

        saved_contratacao = await contratacao_repository.get_by_id(
            contratacao.numero_controle_pncp
        )
        print("Saved Contratacao: ")
        print(saved_contratacao)

        for item in saved_contratacao.items:
            print(item)

    finally:
        await close_db()


async def test_get_updated_contratacoes():
    adapter = PNCPContratacoesSourceAdapter()
    params: PNCPUpdatedContratacoesParams = {
        "dataInicial": YearMonthDay("20250812"),
        "dataFinal": YearMonthDay("20250812"),
        "codigoModalidadeContratacao": ModalidadeId.PREGAO_ELETRONICO,
        "pagina": 1,
        "tamanhoPagina": 10,
    }
    contratacoes = await adapter.get_updated(params)
    print(contratacoes)


if __name__ == "__main__":
    asyncio.run(test_get_contratacao())
