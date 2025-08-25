from tortoise import Tortoise, run_async
from licitabot.config import settings

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": settings.POSTGRES_DB,
                "host": settings.POSTGRES_HOST,
                "password": settings.POSTGRES_PASSWORD,
                "port": settings.POSTGRES_PORT,
                "user": settings.POSTGRES_USER,
                "maxsize": 20,  # pool size
            },
        }
    },
    "apps": {
        "models": {
            "models": ["licitabot.infrastructure.models"]
            + (["aerich.models"] if settings.INIT_DB else []),
            "default_connection": "default",
        },
    },
    "use_tz": False,
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)


async def close_db():
    await Tortoise.close_connections()


# handy CLI for quick testing
if __name__ == "__main__":

    async def main():
        await init_db()
        print("Connected. Models:", Tortoise.apps.get("models").keys())
        await close_db()

    run_async(main())
