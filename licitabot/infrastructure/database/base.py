from sqlalchemy.ext.declarative import declarative_base
import logging
from licitabot.infrastructure.database.session import get_engine

Base = declarative_base()

logger = logging.getLogger("licitabot")


async def initialize_database():

    try:
        logger.info("[*] Initializing database...")
        engine = await get_engine()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("[*] Database initialized successfully")
    except Exception as e:
        logger.error(f"[!] Error initializing database: {e}")
        raise e
