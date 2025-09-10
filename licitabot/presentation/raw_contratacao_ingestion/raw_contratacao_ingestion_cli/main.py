import argparse
import asyncio
from datetime import datetime, timedelta
from licitabot.infrastructure.database.session import create_session
from licitabot.domain.value_objects import CodigoModalidadeContratacao
from licitabot.application.dtos import RawContratacaoIngestionParamsDTO
from licitabot.application.service_factory import ServiceFactory
from licitabot.application.bootstrap import ApplicationBootstrap
from licitabot.settings import logger, settings


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid date format: {date_str}. Use YYYYMMDD or YYYY-MM-DD"
            )


def format_date(date_obj):
    return date_obj.strftime("%Y%m%d")


def get_default_dates(data_final=None):
    if data_final is None:
        data_final = datetime.now()
    data_inicial = data_final - timedelta(
        days=settings.RAW_CONTRATACAO_INGESTION_DEFAULT_DELTA
    )
    return data_inicial, data_final


async def async_main():
    await ApplicationBootstrap.bootstrap()

    parser = argparse.ArgumentParser(description="Raw Contratacao Ingestion CLI")
    parser.add_argument(
        "--dataInicial", type=parse_date, help="Initial date (YYYYMMDD or YYYY-MM-DD)"
    )
    parser.add_argument(
        "--dataFinal", type=parse_date, help="Final date (YYYYMMDD or YYYY-MM-DD)"
    )

    args = parser.parse_args()

    data_inicial, data_final = get_default_dates(args.dataFinal)

    if args.dataInicial:
        data_inicial = args.dataInicial

    logger.info(
        f"[*] Starting raw contratacao ingestion with dataInicial: {data_inicial} and dataFinal: {data_final}"
    )

    session = await create_session()
    async with session:
        raw_contratacao_ingestion_service = (
            ServiceFactory.create_raw_contratacao_ingestion_service(
                session, CodigoModalidadeContratacao.PREGAO_ELETRONICO
            )
        )
        await raw_contratacao_ingestion_service.run(
            RawContratacaoIngestionParamsDTO(
                dataInicial=format_date(data_inicial),
                dataFinal=format_date(data_final),
            )
        )


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
