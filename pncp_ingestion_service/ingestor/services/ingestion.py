# pncp_ingestion_service/ingestor/services/ingestion.py
"""
Funções de ingestão da API PNCP.

Regras:
• `data_ini` e `data_fim` chegam **sempre** como strings ISO-local
  `YYYY-MM-DDTHH:MM:SS` geradas pelo consumer.
• Endpoint PNCP aceita apenas AAAAMMDD, portanto requisitamos
  o(s) dia(s) inteiros e filtramos em memória pelo campo
  `dataAtualizacaoGlobal` (datetime de segundo).
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from httpx import AsyncClient, Timeout, HTTPStatusError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from config import (
    BASE_CONSULTA_URL,
    BASE_ITENS_URL,
    HTTP_TIMEOUT,
    MODALIDADE_CONTRATACAO,
    PAGE_SIZE,
)
from models.pncp import Contratacao, ItemContratacao
from utils import iso_to_ymd, parse_numero_controle

TIMEOUT = Timeout(HTTP_TIMEOUT)


# ───────────────────────────────────────── helpers


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(HTTPStatusError),
    reraise=True,
)
async def _make_request_with_retry(client: AsyncClient, url: str, params: dict = None):
    """Make HTTP request with retry logic for rate limiting."""
    r = await client.get(url, params=params)
    r.raise_for_status()
    return r


async def _total_paginas(client: AsyncClient, di: str, df: str) -> int:
    params = dict(
        dataInicial=di,
        dataFinal=df,
        codigoModalidadeContratacao=MODALIDADE_CONTRATACAO,
        pagina=1,
        tamanhoPagina=PAGE_SIZE,  # Usar o mesmo PAGE_SIZE para consistência
    )

    print(f"[DEBUG] Getting total pages with params: {params}")

    r = await _make_request_with_retry(client, BASE_CONSULTA_URL, params)

    result = r.json()
    total_paginas = result["totalPaginas"]
    print(f"[DEBUG] Total pages: {total_paginas}")

    return total_paginas


async def _fetch_pagina(
    client: AsyncClient, di: str, df: str, pag: int
) -> List[Contratacao]:
    params = dict(
        dataInicial=di,
        dataFinal=df,
        codigoModalidadeContratacao=MODALIDADE_CONTRATACAO,
        pagina=pag,
        tamanhoPagina=PAGE_SIZE,
    )

    print(f"[DEBUG] Fetching page {pag} with params: {params}")

    r = await _make_request_with_retry(client, BASE_CONSULTA_URL, params)
    return [Contratacao(**d) for d in r.json()["data"]]


async def _fetch_itens(client: AsyncClient, num_ctrl: str) -> List[ItemContratacao]:
    cnpj, ano, seq = parse_numero_controle(num_ctrl)
    url = BASE_ITENS_URL.format(cnpj=cnpj, ano=ano, seq=seq)

    try:
        r = await _make_request_with_retry(client, url)
        return [ItemContratacao(**i) for i in r.json()]
    except HTTPStatusError as e:
        if e.response.status_code == 429:
            print(f"[⚠️] Rate limited for {num_ctrl}, skipping...")
            return []
        raise


# ───────────────────────────────────────── função pública


async def ingest_window(data_ini: str, data_fim: str) -> None:
    """
    Ingestão dentro da janela [data_ini, data_fim] (ISO-local, segundo).

    O caller (consumer) garante que ambas as datas são válidas,
    em horário local, e que `data_ini <= data_fim`.
    """
    dt_ini = datetime.fromisoformat(data_ini)
    dt_fim = datetime.fromisoformat(data_fim)

    di_ymd = iso_to_ymd(data_ini)  # para o endpoint
    df_ymd = iso_to_ymd(data_fim)

    print(f"[DEBUG] Processing window: {data_ini} → {data_fim}")
    print(f"[DEBUG] Date range for API: {di_ymd} → {df_ymd}")

    async with AsyncClient(timeout=TIMEOUT) as client:
        tot = await _total_paginas(client, di_ymd, df_ymd)

        for pag in range(tot, 0, -1):  # páginas da mais nova → antiga
            contratos = await _fetch_pagina(client, di_ymd, df_ymd, pag)

            for c in contratos[::-1]:  # item final é o mais recente
                dt_c = c.data_atualizacao_global  # Pydantic já converteu para datetime

                if dt_c < dt_ini:  # alcançou o passado da janela
                    return
                if dt_c > dt_fim:  # registro futuro (mesmo dia)
                    continue

                itens = await _fetch_itens(client, c.numero_controle_pncp)

                # TODO: persistir ou repassar
                print(f"[✓] {c.numero_controle_pncp} {dt_c} — " f"{len(itens)} itens")
