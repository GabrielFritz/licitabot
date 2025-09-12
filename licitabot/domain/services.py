from datetime import datetime
from zoneinfo import ZoneInfo


class BrazilianTimeService:

    timezone = ZoneInfo("America/Sao_Paulo")

    def get_timezone(self):
        return self.timezone

    def get_datetime_now(self):
        return datetime.now(self.timezone)


time_service = BrazilianTimeService()
