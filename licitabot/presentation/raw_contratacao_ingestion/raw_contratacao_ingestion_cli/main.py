import argparse
import asyncio
from datetime import datetime
from licitabot.presentation.raw_contratacao_ingestion.raw_contratacao_ingestion_consumer.publish import (
    publish_raw_contratacao_ingestion_message,
)


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


async def async_main():

    parser = argparse.ArgumentParser(description="Raw Contratacao Ingestion CLI")
    parser.add_argument(
        "--dataInicial", type=parse_date, help="Initial date (YYYYMMDD or YYYY-MM-DD)"
    )
    parser.add_argument(
        "--dataFinal", type=parse_date, help="Final date (YYYYMMDD or YYYY-MM-DD)"
    )

    args = parser.parse_args()

    data_inicial = args.dataInicial
    data_final = args.dataFinal

    await publish_raw_contratacao_ingestion_message(data_inicial, data_final)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
