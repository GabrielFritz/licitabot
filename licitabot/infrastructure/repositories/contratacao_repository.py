from tortoise.transactions import in_transaction

from licitabot.domain.entities import Contratacao
from licitabot.infrastructure.models.contratacao import (
    Contratacao as ContratacaoSchema,
)
from licitabot.infrastructure.repositories.simple_repositories import (
    OrgaoEntidadeRepository,
    UnidadeOrgaoRepository,
    AmparoLegalRepository,
    FonteOrcamentariaRepository,
)
from licitabot.infrastructure.repositories.base_repository import BaseRepository
from licitabot.infrastructure.repositories.item_contratacao_repository import (
    ItemContratacaoRepository,
)


class ContratacaoRepository(BaseRepository[Contratacao, ContratacaoSchema]):
    pydantic_model = Contratacao
    tortoise_model = ContratacaoSchema
    pk_field = "numero_controle_pncp"
    related_fields = [
        "orgao_entidade",
        "unidade_orgao",
        "unidade_sub_rogada",
        "orgao_sub_rogado",
        "amparo_legal",
    ]
    prefetch_fields = ["items", "fontes_orcamentarias"] + [
        f"items__{field}" for field in ItemContratacaoRepository.related_fields
    ]

    orgao_entidade_repository: OrgaoEntidadeRepository = OrgaoEntidadeRepository()
    unidade_orgao_repository: UnidadeOrgaoRepository = UnidadeOrgaoRepository()
    unidade_sub_rogada_repository: UnidadeOrgaoRepository = UnidadeOrgaoRepository()
    orgao_sub_rogado_repository: OrgaoEntidadeRepository = OrgaoEntidadeRepository()
    amparo_legal_repository: AmparoLegalRepository = AmparoLegalRepository()
    fonte_orcamentaria_repository: FonteOrcamentariaRepository = (
        FonteOrcamentariaRepository()
    )
    item_contratacao_repository: ItemContratacaoRepository = ItemContratacaoRepository()

    async def create(self, entity: Contratacao) -> None:
        contratacao_items = entity.items
        async with in_transaction():
            await self._save_related_entities(entity)
            entity_orm = await self._to_orm(entity)
            result = await self.tortoise_model.create(**entity_orm)

            await self._save_many_to_many_entities(entity, result)

            for item_contratacao in contratacao_items:
                await self.item_contratacao_repository.save(item_contratacao)

    async def update(self, entity: Contratacao) -> None:
        contratacao_items = entity.items
        async with in_transaction():
            await self._save_related_entities(entity)
            entity_orm = await self._to_orm(entity)
            entity_orm.pop(self.pk_field, None)
            await self.tortoise_model.filter(
                **{self.pk_field: getattr(entity, self.pk_field)}
            ).update(**entity_orm)
            result = await self.get_by_id(
                getattr(entity, self.pk_field), mode="tortoise"
            )
            await self._save_many_to_many_entities(entity, result)
            for item_contratacao in contratacao_items:
                await self.item_contratacao_repository.save(item_contratacao)

    async def _save_related_entities(self, entity: Contratacao) -> None:
        orgao_entidade_entity = entity.orgao_entidade
        unidade_orgao_entity = entity.unidade_orgao
        unidade_sub_rogada_entity = entity.unidade_sub_rogada
        orgao_sub_rogado_entity = entity.orgao_sub_rogado
        amparo_legal_entity = entity.amparo_legal
        fontes_orcamentarias_entity = entity.fontes_orcamentarias

        if orgao_entidade_entity:
            await self.orgao_entidade_repository.save(orgao_entidade_entity)
        if unidade_orgao_entity:
            await self.unidade_orgao_repository.save(unidade_orgao_entity)
        if unidade_sub_rogada_entity:
            await self.unidade_sub_rogada_repository.save(unidade_sub_rogada_entity)
        if orgao_sub_rogado_entity:
            await self.orgao_sub_rogado_repository.save(orgao_sub_rogado_entity)
        if amparo_legal_entity:
            await self.amparo_legal_repository.save(amparo_legal_entity)
        if fontes_orcamentarias_entity:
            for fonte_orcamentaria_entity in fontes_orcamentarias_entity:
                await self.fonte_orcamentaria_repository.save(fonte_orcamentaria_entity)

    async def _save_many_to_many_entities(
        self, entity: Contratacao, result: ContratacaoSchema
    ) -> None:
        if entity.fontes_orcamentarias:
            for fonte in entity.fontes_orcamentarias:
                fonte_orm = await self.fonte_orcamentaria_repository.get_by_id(
                    getattr(fonte, self.fonte_orcamentaria_repository.pk_field),
                    mode="tortoise",
                )
                if fonte_orm:
                    await result.fontes_orcamentarias.add(fonte_orm)

    async def _to_orm(self, entity: Contratacao) -> dict:

        entity_dump = entity.model_dump()
        entity_dump.pop("fontes_orcamentarias", None)
        entity_dump.pop("items", None)

        entity_dump.pop("orgao_entidade", None)
        entity_dump.pop("unidade_orgao", None)
        entity_dump.pop("unidade_sub_rogada", None)
        entity_dump.pop("orgao_sub_rogado", None)
        entity_dump.pop("amparo_legal", None)

        entity_dump["modalidade_id"] = (
            entity.modalidade_id.value if entity.modalidade_id else None
        )
        entity_dump["situacao_compra_id"] = (
            entity.situacao_compra_id.value if entity.situacao_compra_id else None
        )
        entity_dump["modo_disputa_id"] = (
            entity.modo_disputa_id.value if entity.modo_disputa_id else None
        )
        entity_dump["tipo_instrumento_convocatorio_codigo"] = (
            entity.tipo_instrumento_convocatorio_codigo.value
            if entity.tipo_instrumento_convocatorio_codigo
            else None
        )
        entity_dump["orgao_entidade_id"] = (
            getattr(entity.orgao_entidade, self.orgao_entidade_repository.pk_field)
            if entity.orgao_entidade
            else None
        )
        entity_dump["unidade_orgao_id"] = (
            getattr(entity.unidade_orgao, self.unidade_orgao_repository.pk_field)
            if entity.unidade_orgao
            else None
        )
        entity_dump["unidade_sub_rogada_id"] = (
            getattr(
                entity.unidade_sub_rogada,
                self.unidade_sub_rogada_repository.pk_field,
            )
            if entity.unidade_sub_rogada
            else None
        )
        entity_dump["orgao_sub_rogado_id"] = (
            getattr(entity.orgao_sub_rogado, self.orgao_sub_rogado_repository.pk_field)
            if entity.orgao_sub_rogado
            else None
        )
        entity_dump["amparo_legal_id"] = (
            getattr(entity.amparo_legal, self.amparo_legal_repository.pk_field)
            if entity.amparo_legal
            else None
        )

        return entity_dump
