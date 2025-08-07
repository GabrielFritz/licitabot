import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from licitabot.application.dtos import PNCPEmbeddingsGenerationRequestDTO
from licitabot.application.dtos import PNCPEmbeddingsGenerationResponseDTO
from licitabot.application.interfaces.repositories import (
    RepositoryInterfaceWithGlobalUpdate,
    RepositoryInterface,
)
from licitabot.application.interfaces.embeddings import PNCPEmbeddingInterface

from licitabot.domain.entities import Contratacao, ItemContratacao
from licitabot.domain.entities.embedding import (
    ContratacaoEmbedding,
    ItemContratacaoEmbedding,
)
import time
import logging

logger = logging.getLogger("licitabot")

semaphore = asyncio.Semaphore(1)


class PNCPEmbeddingsGenerationService:

    def __init__(
        self,
        session: AsyncSession,
        contratacao_repository: RepositoryInterfaceWithGlobalUpdate[Contratacao],
        item_contratacao_repository: RepositoryInterfaceWithGlobalUpdate[
            ItemContratacao
        ],
        contratacao_embedding_repository: RepositoryInterface[ContratacaoEmbedding],
        item_contratacao_embedding_repository: RepositoryInterface[
            ItemContratacaoEmbedding
        ],
        embedding: PNCPEmbeddingInterface,
    ):
        self.session = session
        self.contratacao_repository = contratacao_repository
        self.item_contratacao_repository = item_contratacao_repository
        self.contratacao_embedding_repository = contratacao_embedding_repository
        self.item_contratacao_embedding_repository = (
            item_contratacao_embedding_repository
        )
        self.embedding = embedding

    async def embed_and_upsert(self, func, repository, *args, **kwargs):
        async with semaphore:
            embedding = await func(*args, **kwargs)
            await repository.upsert(embedding)

    async def run(self, request: PNCPEmbeddingsGenerationRequestDTO):

        start_time = time.time()

        try:
            contratacoes_to_embed = (
                await self.contratacao_repository.get_by_global_update_between(
                    request.data_ini, request.data_fim
                )
            )
            item_contratacoes_to_embed = (
                await self.item_contratacao_repository.get_by_global_update_between(
                    request.data_ini, request.data_fim
                )
            )

            logger.info(
                f"Generating embeddings for {len(contratacoes_to_embed)} contratacoes and {len(item_contratacoes_to_embed)} item_contratacoes"
            )

            logger.info(f"Contratacoes to embed: {len(contratacoes_to_embed)}")

            embedding_tasks = [
                self.embed_and_upsert(
                    self.embedding.embed_contratacao,
                    self.contratacao_embedding_repository,
                    contratacao,
                )
                for contratacao in contratacoes_to_embed
            ]
            await asyncio.gather(*embedding_tasks)

            logger.info(
                f"Item contratacoes to embed: {len(item_contratacoes_to_embed)}"
            )

            embedding_tasks = [
                self.embed_and_upsert(
                    self.embedding.embed_item_contratacao,
                    self.item_contratacao_embedding_repository,
                    item_contratacao,
                )
                for item_contratacao in item_contratacoes_to_embed
            ]
            await asyncio.gather(*embedding_tasks)

            return PNCPEmbeddingsGenerationResponseDTO(
                success=True,
                message=f"PNCP embeddings generation from {request.data_ini} to {request.data_fim} completed successfully",
                embeddings_contratacao_gerados=len(contratacoes_to_embed),
                embeddings_item_contratacao_gerados=len(item_contratacoes_to_embed),
                erros=[],
                tempo_processamento=time.time() - start_time,
            )
        except Exception as e:
            import traceback

            logger.error(f"Error in PNCP embeddings generation: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise e
            return PNCPEmbeddingsGenerationResponseDTO(
                success=False,
                message=f"PNCP embeddings generation from {request.data_ini} to {request.data_fim} failed",
                embeddings_contratacao_gerados=0,
                embeddings_item_contratacao_gerados=0,
                erros=[str(e)],
                tempo_processamento=time.time() - start_time,
            )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
