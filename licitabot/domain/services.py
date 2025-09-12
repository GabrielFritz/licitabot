from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from licitabot.domain.value_objects import IngestionWindow
from licitabot.settings import settings


class BrazilianTimeService:

    timezone = ZoneInfo("America/Sao_Paulo")

    def get_timezone(self):
        return self.timezone

    def get_datetime_now(self):
        return datetime.now(self.timezone)


class IngestionWindowService:

    def __init__(self, time_service: BrazilianTimeService, delta_days: int):
        self.time_service = time_service
        self.delta_days = delta_days

    def get_ingestion_window(
        self, data_inicial: datetime = None, data_final: datetime = None
    ):
        if data_inicial is not None and data_final is not None:
            return IngestionWindow.from_datetime(data_inicial, data_final)
        elif data_inicial is not None:
            data_final = self.time_service.get_datetime_now()
            return IngestionWindow.from_datetime(data_inicial, data_final)
        elif data_final is not None:
            data_inicial = data_final - timedelta(days=self.delta_days)
            return IngestionWindow.from_datetime(data_inicial, data_final)
        else:
            data_final = self.time_service.get_datetime_now()
            data_inicial = data_final - timedelta(days=self.delta_days)
            return IngestionWindow.from_datetime(data_inicial, data_final)


time_service = BrazilianTimeService()
ingestion_window_service = IngestionWindowService(
    time_service, settings.ingestion_services.default_delta_days
)
