import os

from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("licitabot")


load_dotenv()


class Settings:
    HTTP_TIMEOUT = 60.0
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "pncp_ingestion")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "pncp_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pncp_pass")
    ASYNC_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?ssl=require"
    SYNC_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?sslmode=require"
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
    INGESTION_WINDOW_DEFAULT_DELTA_DAYS = int(
        os.getenv("INGESTION_WINDOW_DEFAULT_DELTA_DAYS", "1")
    )


settings = Settings()
