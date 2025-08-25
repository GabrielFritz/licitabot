from tortoise.transactions import in_transaction
from licitabot.infrastructure.repositories.base_repository import BaseRepository
from licitabot.domain.entities import ItemContratacao
from licitabot.infrastructure.models.item_contratacao import (
    ItemContratacao as ItemContratacaoSchema,
)
from licitabot.infrastructure.repositories.simple_repositories import (
    TipoMargemPreferenciaRepository,
    CatalogoRepository,
    CategoriaItemCatalogoRepository,
)


class ItemContratacaoRepository(BaseRepository[ItemContratacao, ItemContratacaoSchema]):
    pydantic_model = ItemContratacao
    tortoise_model = ItemContratacaoSchema
    pk_field = "item_id"
    related_fields = [
        "tipo_margem_preferencia",
        "catalogo",
        "categoria_item_catalogo",
    ]

    tipo_margem_preferencia_repository: TipoMargemPreferenciaRepository = (
        TipoMargemPreferenciaRepository()
    )
    catalogo_repository: CatalogoRepository = CatalogoRepository()
    categoria_item_catalogo_repository: CategoriaItemCatalogoRepository = (
        CategoriaItemCatalogoRepository()
    )

    async def create(self, entity: ItemContratacao) -> None:
        async with in_transaction():
            await self._save_related_entities(entity)
            entity_orm = await self._to_orm(entity)

            await self.tortoise_model.create(**entity_orm)

    async def update(self, entity: ItemContratacao) -> None:
        async with in_transaction():
            await self._save_related_entities(entity)

            entity_orm = await self._to_orm(entity)
            entity_orm.pop(self.pk_field, None)
            await self.tortoise_model.filter(
                **{self.pk_field: getattr(entity, self.pk_field)}
            ).update(**entity_orm)

    async def _save_related_entities(self, entity: ItemContratacao) -> None:
        tipo_margem_preferencia_entity = entity.tipo_margem_preferencia
        catalogo_entity = entity.catalogo
        categoria_item_catalogo_entity = entity.categoria_item_catalogo

        if tipo_margem_preferencia_entity:
            await self.tipo_margem_preferencia_repository.save(
                tipo_margem_preferencia_entity
            )
        if catalogo_entity:
            await self.catalogo_repository.save(catalogo_entity)
        if categoria_item_catalogo_entity:
            await self.categoria_item_catalogo_repository.save(
                categoria_item_catalogo_entity
            )

    async def _to_orm(self, entity: ItemContratacao) -> dict:

        entity_dump = entity.model_dump()
        entity_dump.pop("contratacao", None)
        entity_dump.pop("tipo_margem_preferencia", None)
        entity_dump.pop("catalogo", None)
        entity_dump.pop("categoria_item_catalogo", None)

        entity_dump["criterio_julgamento_id"] = (
            entity.criterio_julgamento_id.value
            if entity.criterio_julgamento_id
            else None
        )
        entity_dump["situacao_compra_item"] = (
            entity.situacao_compra_item.value if entity.situacao_compra_item else None
        )
        entity_dump["tipo_beneficio"] = (
            entity.tipo_beneficio.value if entity.tipo_beneficio else None
        )
        entity_dump["material_ou_servico"] = (
            entity.material_ou_servico.value if entity.material_ou_servico else None
        )

        entity_dump["contratacao_id"] = entity.numero_controle_pncp

        entity_dump["tipo_margem_preferencia_id"] = (
            getattr(
                entity.tipo_margem_preferencia,
                self.tipo_margem_preferencia_repository.pk_field,
            )
            if entity.tipo_margem_preferencia
            else None
        )

        entity_dump["catalogo_id"] = (
            getattr(entity.catalogo, self.catalogo_repository.pk_field)
            if entity.catalogo
            else None
        )
        entity_dump["categoria_item_catalogo_id"] = (
            getattr(
                entity.categoria_item_catalogo,
                self.categoria_item_catalogo_repository.pk_field,
            )
            if entity.categoria_item_catalogo
            else None
        )

        return entity_dump
