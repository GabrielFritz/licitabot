"""
Serviço de persistência para dados da API PNCP.

Orquestra a persistência de contratações com todos os seus relacionamentos:
- Órgãos e entidades
- Unidades de órgãos
- Amparos legais
- Fontes orçamentárias
- Contratações
- Itens de contratação
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ingestor.database.connection import get_async_session
from ingestor.database.repositories import (
    OrgaoRepository,
    UnidadeRepository,
    ContratacaoRepository,
    ItemRepository,
)
from ingestor.models.pncp import (
    Contratacao as ContratacaoPydantic,
    ItemContratacao as ItemContratacaoPydantic,
)


@dataclass
class PersistenceResult:
    """Resultado de uma operação de persistência."""

    success: bool
    numero_controle_pncp: Optional[str] = None
    itens_saved: int = 0
    orgao_upserted: bool = False
    unidade_upserted: bool = False
    amparo_upserted: bool = False
    fontes_upserted: int = 0
    errors: List[str] = field(default_factory=list)
    duration_ms: float = 0.0

    def add_error(self, error: str):
        """Adiciona erro à lista."""
        self.errors.append(error)

    def is_success(self) -> bool:
        """Verifica se a operação foi bem-sucedida."""
        return self.success and len(self.errors) == 0


async def persist_contratacao_with_items(
    contratacao: ContratacaoPydantic, itens: List[ItemContratacaoPydantic]
) -> PersistenceResult:
    """
    Persiste uma contratação com todos os seus itens.

    Fluxo:
    1. Normalizar dados da contratação
    2. Upsert órgão e unidade
    3. Upsert amparo legal e fontes orçamentárias
    4. Upsert contratação
    5. Upsert todos os itens
    6. Commit transação

    Args:
        contratacao: Dados da contratação vindos da API
        itens: Lista de itens da contratação

    Returns:
        PersistenceResult com informações da operação
    """
    start_time = time.time()
    result = PersistenceResult(success=False)

    try:
        async with get_async_session() as session:
            # Inicializa repositórios
            orgao_repo = OrgaoRepository(session)
            unidade_repo = UnidadeRepository(session)
            contratacao_repo = ContratacaoRepository(session)
            item_repo = ItemRepository(session)

            # 1. Upsert órgão
            orgao_id = None
            try:
                orgao = await orgao_repo.upsert(contratacao.orgao_entidade)
                if orgao and orgao.id:
                    orgao_id = orgao.id
                    result.orgao_upserted = True
            except Exception as e:
                result.add_error(f"Erro ao salvar órgão: {e}")

            # 2. Upsert unidade
            unidade_id = None
            try:
                unidade = await unidade_repo.upsert(contratacao.unidade_orgao)
                if unidade and unidade.id:
                    unidade_id = unidade.id
                    result.unidade_upserted = True
            except Exception as e:
                result.add_error(f"Erro ao salvar unidade: {e}")

            # 3. Upsert órgão sub-rogado (se existir)
            orgao_sub_rogado_id = None
            if contratacao.orgao_sub_rogado:
                try:
                    orgao_sub_rogado = await orgao_repo.upsert(
                        contratacao.orgao_sub_rogado
                    )
                    if orgao_sub_rogado and orgao_sub_rogado.id:
                        orgao_sub_rogado_id = orgao_sub_rogado.id
                except Exception as e:
                    result.add_error(f"Erro ao salvar órgão sub-rogado: {e}")

            # 4. Upsert unidade sub-rogada (se existir)
            unidade_sub_rogada_id = None
            if contratacao.unidade_sub_rogada:
                try:
                    unidade_sub_rogada = await unidade_repo.upsert(
                        contratacao.unidade_sub_rogada
                    )
                    if unidade_sub_rogada and unidade_sub_rogada.id:
                        unidade_sub_rogada_id = unidade_sub_rogada.id
                except Exception as e:
                    result.add_error(f"Erro ao salvar unidade sub-rogada: {e}")

            # 5. Upsert amparo legal
            amparo_id = None
            try:
                amparo = await contratacao_repo.upsert_amparo_legal(
                    contratacao.amparo_legal
                )
                if amparo and amparo.id:
                    amparo_id = amparo.id
                    result.amparo_upserted = True
            except Exception as e:
                result.add_error(f"Erro ao salvar amparo legal: {e}")

            # 6. Upsert fontes orçamentárias
            fontes_salvas = 0
            for fonte in contratacao.fontes_orcamentarias:
                try:
                    await contratacao_repo.upsert_fonte_orcamentaria(fonte)
                    fontes_salvas += 1
                except Exception as e:
                    result.add_error(
                        f"Erro ao salvar fonte orçamentária {fonte.codigo}: {e}"
                    )
            result.fontes_upserted = fontes_salvas

            # 7. Upsert contratação (mesmo se alguns relacionamentos falharam)
            try:
                contratacao_salva = await contratacao_repo.upsert(
                    contratacao,
                    orgao_id,
                    unidade_id,
                    amparo_id,
                    unidade_sub_rogada_id,
                    orgao_sub_rogado_id,
                )
                result.numero_controle_pncp = contratacao_salva.numero_controle_pncp
            except Exception as e:
                result.add_error(f"Erro ao salvar contratação: {e}")
                return result

            # 8. Upsert itens
            try:
                itens_salvos = await item_repo.upsert_batch(
                    itens, contratacao_salva.numero_controle_pncp
                )
                result.itens_saved = len(itens_salvos)
            except Exception as e:
                result.add_error(f"Erro ao salvar itens: {e}")
                return result

            # 7. Commit transação
            await session.commit()

            # 8. Calcula duração
            result.duration_ms = (time.time() - start_time) * 1000
            result.success = True

            return result

    except Exception as e:
        result.add_error(f"Erro geral na persistência: {e}")
        return result


async def persist_batch(
    contratacoes_with_items: List[
        tuple[ContratacaoPydantic, List[ItemContratacaoPydantic]]
    ],
) -> List[PersistenceResult]:
    """
    Persiste um lote de contratações com seus itens.

    Args:
        contratacoes_with_items: Lista de tuplas (contratacao, itens)

    Returns:
        Lista de PersistenceResult
    """
    results = []

    for contratacao, itens in contratacoes_with_items:
        result = await persist_contratacao_with_items(contratacao, itens)
        results.append(result)

    return results


def format_persistence_log(result: PersistenceResult, numero_controle: str) -> str:
    """
    Formata log de persistência.

    Args:
        result: Resultado da persistência
        numero_controle: Número de controle da contratação

    Returns:
        String formatada para log
    """
    if result.is_success():
        status = "✓"
        details = f"{result.itens_saved} itens salvos"
        if result.orgao_upserted:
            details += " (orgao:✓"
        if result.unidade_upserted:
            details += ", unidade:✓"
        if result.amparo_upserted:
            details += ", amparo:✓"
        if result.fontes_upserted > 0:
            details += f", fontes:{result.fontes_upserted}"
        details += f", duration:{result.duration_ms:.0f}ms)"

        return f"[PERSIST] {status} {numero_controle} — {details}"
    else:
        status = "❌"
        errors = "; ".join(result.errors[:2])  # Limita a 2 erros
        if len(result.errors) > 2:
            errors += f" (+{len(result.errors) - 2} mais)"

        return f"[PERSIST] {status} {numero_controle} — Falha: {errors}"
