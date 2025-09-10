from faststream import Logger
from faststream.rabbit import RabbitRouter
from licitabot.application.service_factory import ServiceFactory
from licitabot.application.dtos import RawContratacaoIngestionParamsDTO
from licitabot.domain.value_objects import YearMonthDay
from pydantic import BaseModel, field_validator, ConfigDict
from licitabot.infrastructure.database.session import create_session
from licitabot.domain.value_objects import CodigoModalidadeContratacao

router = RabbitRouter()


class RawContratacaoIngestionMessageDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    dataInicial: YearMonthDay
    dataFinal: YearMonthDay

    @field_validator("dataInicial", "dataFinal", mode="before")
    @classmethod
    def validate_year_month_day(cls, v):
        if isinstance(v, str):
            return YearMonthDay(v)
        return v


@router.subscriber("raw_contratacao_ingestion_triggered")
async def handle_raw_contratacao_ingestion_triggered(
    message: RawContratacaoIngestionMessageDTO, logger: Logger
):
    logger.info(f"[*] Received raw contratacao ingestion request: {message}")

    raw_contratacao_ingestion_request = RawContratacaoIngestionParamsDTO(
        dataInicial=message.dataInicial,
        dataFinal=message.dataFinal,
    )
    session = await create_session()

    async with session:

        raw_contratacao_ingestion_service = (
            ServiceFactory.create_raw_contratacao_ingestion_service(
                session, CodigoModalidadeContratacao.PREGAO_ELETRONICO
            )
        )

        await raw_contratacao_ingestion_service.run(raw_contratacao_ingestion_request)

    logger.info(
        f"[*] Raw contratacao ingestion request processed successfully: {message}"
    )
