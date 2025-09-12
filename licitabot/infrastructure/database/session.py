from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from licitabot.settings import settings

engine = create_async_engine(settings.database.async_url)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession)


async def get_session():
    async with async_session_factory() as session:
        yield session


async def create_session() -> AsyncSession:
    return async_session_factory()


async def get_engine():
    return engine
