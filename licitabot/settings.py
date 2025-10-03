import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("licitabot")


class DatabaseSettings(BaseModel):

    host: str = "localhost"
    port: int = 5432
    db: str = "pncp_ingestion"
    user: str = "pncp_user"
    password: str = "pncp_pass"

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}?ssl=prefer"

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}?sslmode=prefer"


class RabbitMQSettings(BaseModel):
    user: str = "guest"
    password: str = "guest"
    host: str = "localhost"
    port: int = 5672
    vhost: str = "/"

    @property
    def amqp_url(self) -> str:
        vhost = self.vhost.lstrip("/")
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{vhost}"


class IngestionServicesSettings(BaseModel):
    default_delta_days: int = 1


class HTTPSettings(BaseModel):
    timeout: float = 60.0


class LiteLLMSettings(BaseModel):
    base_url: str = "os.environ/LITELLM__BASE_URL"
    api_key: str = "os.environ/LITELLM__API_KEY"


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    database: DatabaseSettings = DatabaseSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    ingestion_services: IngestionServicesSettings = IngestionServicesSettings()
    http: HTTPSettings = HTTPSettings()
    litellm: LiteLLMSettings = LiteLLMSettings()


settings = Settings()
