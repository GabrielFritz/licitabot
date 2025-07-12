# pncp_ingestion_service/ingestor/consumer.py
"""
Worker que escuta a fila `ingest.pncp` e dispara ingestão do PNCP.

Modos aceitos na mensagem (JSON):
• {}  ou {"mode":"update"}
      → janela automática: últimos ROLLING_WINDOW_MINUTES (padrão 15 min)
• {"mode":"backfill",
     "data_ini":"2025-07-10T12:00:00",
     "data_fim":"2025-07-10T18:00:00"}
      → ingere intervalo explícito
Observação: datas em formato ISO **sem** timezone (YYYY-MM-DDTHH:MM:SS),
considerando horário local (America/Cuiabá implícito).
"""

import asyncio
import json
from datetime import datetime, timedelta

from aio_pika import IncomingMessage, connect_robust

from config import settings
from services.ingestion import ingest_window
from utils import format_iso_local


async def handle(message: IncomingMessage) -> None:
    async with message.process():
        # ── 1. Decodifica JSON (se houver)
        try:
            payload = json.loads(message.body.decode()) if message.body else {}
        except json.JSONDecodeError:
            payload = {}

        mode = payload.get("mode", "update")

        if mode == "backfill":
            # parâmetros obrigatórios no payload
            data_ini = payload["data_ini"]
            data_fim = payload["data_fim"]
        else:  # mode == "update"
            dt_fim = datetime.now().replace(microsecond=0)
            dt_ini = dt_fim - timedelta(minutes=settings.ROLLING_WINDOW_MINUTES)
            data_ini = format_iso_local(dt_ini)
            data_fim = format_iso_local(dt_fim)

        delta_sec = int(
            (
                datetime.fromisoformat(data_fim) - datetime.fromisoformat(data_ini)
            ).total_seconds()
        )

        print(
            f"[ingestor] mode={mode}  window={data_ini} → {data_fim}  "
            f"(Δ={delta_sec}s)"
        )

        await ingest_window(data_fim=data_fim, data_ini=data_ini)


async def main() -> None:
    connection = await connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(settings.QUEUE_NAME, durable=True)
    await queue.consume(handle)

    print(f"[*] Listening on {settings.QUEUE_NAME} …  Ctrl-C para sair")
    await asyncio.Future()  # mantém o loop vivo


if __name__ == "__main__":
    asyncio.run(main())
