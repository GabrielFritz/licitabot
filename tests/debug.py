import asyncio
from licitabot.infrastructure.repositories.item_contratacao.repository import (
    ItemContratacaoReadOnlyRepository,
)
from licitabot.infrastructure.database.session import create_session
from licitabot.domain.value_objects import NumeroControlePNCP


async def main():
    async with await create_session() as session:
        repository = ItemContratacaoReadOnlyRepository(session)
        item_contratacao = await repository.get(
            NumeroControlePNCP("17935388000115-1-000095/2025"), 159
        )
        print(item_contratacao)


if __name__ == "__main__":
    asyncio.run(main())
