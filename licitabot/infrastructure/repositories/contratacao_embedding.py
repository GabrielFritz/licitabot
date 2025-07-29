from typing import Any, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from licitabot.application.interfaces.repositories import RepositoryInterface
from licitabot.domain.entities.embedding import ContratacaoEmbedding
from licitabot.infrastructure.repositories.database_schemas import (
    ContratacaoEmbedding as ContratacaoEmbeddingSchema,
)


class ContratacaoEmbeddingRepository(RepositoryInterface[ContratacaoEmbedding]):
    """Repository for contratacao embeddings."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: Any) -> Optional[ContratacaoEmbedding]:
        db_result = await self._get_by_id(entity_id)
        if db_result:
            return ContratacaoEmbedding.model_validate(db_result)
        return None

    async def upsert(self, entity: ContratacaoEmbedding) -> ContratacaoEmbedding:
        db_result = await self._upsert(entity)
        return ContratacaoEmbedding.model_validate(db_result)

    async def delete(self, entity_id: Any) -> bool:
        embedding_schema = await self._get_by_id(entity_id)
        if embedding_schema:
            self.session.delete(embedding_schema)
            await self.session.commit()
            return True
        return False

    async def list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[ContratacaoEmbedding]:
        db_results = await self._list_all(limit, offset)
        return [ContratacaoEmbedding.model_validate(item) for item in db_results]

    async def count_all(self) -> int:
        query = select(func.count(ContratacaoEmbeddingSchema.numero_controle_pncp))
        result = await self.session.execute(query)
        return result.scalar()

    async def _get_by_id(self, entity_id: Any) -> Optional[ContratacaoEmbeddingSchema]:
        query = select(ContratacaoEmbeddingSchema).where(
            ContratacaoEmbeddingSchema.numero_controle_pncp == entity_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[ContratacaoEmbeddingSchema]:
        query = (
            select(ContratacaoEmbeddingSchema)
            .order_by(ContratacaoEmbeddingSchema.numero_controle_pncp)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def _upsert(self, entity: ContratacaoEmbedding) -> ContratacaoEmbeddingSchema:
        embedding_existente = await self._get_by_id(entity.numero_controle_pncp)
        dados_embedding = entity.model_dump()

        if embedding_existente:
            for key, value in dados_embedding.items():
                setattr(embedding_existente, key, value)
            entidade = embedding_existente
        else:
            entidade = ContratacaoEmbeddingSchema(**dados_embedding)
            self.session.add(entidade)

        await self.session.commit()
        await self.session.refresh(entidade)
        return entidade
