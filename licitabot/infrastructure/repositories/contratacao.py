from typing import List, Optional

from licitabot.application.interfaces.repositories import (
    RepositoryInterfaceWithGlobalUpdate,
)
from licitabot.domain.entities import (
    AmparoLegal,
    Contratacao,
    OrgaoEntidade,
    UnidadeOrgao,
)
from licitabot.infrastructure.repositories.amparo_legal import (
    AmparoLegalRepository,
)
from licitabot.infrastructure.repositories.database_schemas import (
    Contratacao as ContratacaoSchema,
)
from licitabot.infrastructure.repositories.fonte_orcamentaria import (
    FonteOrcamentariaRepository,
)
from licitabot.infrastructure.repositories.orgao_entidade import (
    OrgaoEntidadeRepository,
)
from licitabot.infrastructure.repositories.unidade_orgao import (
    UnidadeOrgaoRepository,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from typing import Any

from sqlalchemy import func

from datetime import datetime
import logging

logger = logging.getLogger("licitabot")


class ContratacaoRepository(RepositoryInterfaceWithGlobalUpdate[Contratacao]):

    def __init__(
        self,
        session: AsyncSession,
        amparo_legal_repository: AmparoLegalRepository,
        fonte_orcamentaria_repository: FonteOrcamentariaRepository,
        orgao_entidade_repository: OrgaoEntidadeRepository,
        unidade_orgao_repository: UnidadeOrgaoRepository,
    ):
        self.session = session
        self.amparo_legal_repository = amparo_legal_repository
        self.fonte_orcamentaria_repository = fonte_orcamentaria_repository
        self.orgao_entidade_repository = orgao_entidade_repository
        self.unidade_orgao_repository = unidade_orgao_repository

    async def get_by_global_update_between(
        self, data_ini: datetime, data_fim: datetime
    ) -> List[Contratacao]:
        db_results = await self._get_by_global_update_between(data_ini, data_fim)
        return [Contratacao.model_validate(item) for item in db_results]

    async def get_by_id(self, entity_id: Any) -> Optional[Contratacao]:
        db_result = await self._get_by_id(entity_id)
        if db_result:
            return Contratacao.model_validate(db_result)
        return None

    async def upsert(self, entity: Contratacao) -> Contratacao:

        orgao_entidade = await self.orgao_entidade_repository.upsert(
            entity.orgao_entidade
        )
        unidade_orgao = await self.unidade_orgao_repository.upsert(entity.unidade_orgao)
        amparo_legal = await self.amparo_legal_repository.upsert(entity.amparo_legal)

        unidade_sub_rogada = None
        if entity.unidade_sub_rogada:
            unidade_sub_rogada = await self.unidade_orgao_repository.upsert(
                entity.unidade_sub_rogada
            )

        orgao_sub_rogado = None
        if entity.orgao_sub_rogado:
            orgao_sub_rogado = await self.orgao_entidade_repository.upsert(
                entity.orgao_sub_rogado
            )

        fontes_orcamentarias = []
        for fonte in entity.fontes_orcamentarias:
            fonte_saved = await self.fonte_orcamentaria_repository.upsert(fonte)
            fontes_orcamentarias.append(fonte_saved)

        upserted_contratacao = await self._upsert(
            entity,
            orgao_entidade_cnpj=orgao_entidade.cnpj,
            unidade_orgao_codigo_unidade=unidade_orgao.codigo_unidade,
            amparo_legal_codigo=amparo_legal.codigo,
            unidade_sub_rogada_codigo_unidade=(
                unidade_sub_rogada.codigo_unidade if unidade_sub_rogada else None
            ),
            orgao_sub_rogado_cnpj=orgao_sub_rogado.cnpj if orgao_sub_rogado else None,
        )

        return Contratacao.model_validate(upserted_contratacao)

    async def delete(self, entity_id: Any) -> bool:
        query = select(ContratacaoSchema).where(
            ContratacaoSchema.numero_controle_pncp == entity_id
        )
        result = await self.session.execute(query)
        contratacao = result.scalar_one_or_none()

        if contratacao:
            self.session.delete(contratacao)
            await self.session.commit()
            return True
        return False

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[Contratacao]:
        db_results = await self._list_all(limit, offset)
        return [Contratacao.model_validate(item) for item in db_results]

    async def count_all(self) -> int:
        query = select(func.count(ContratacaoSchema.numero_controle_pncp))
        result = await self.session.execute(query)
        return result.scalar()

    async def _get_by_global_update_between(
        self, data_ini: datetime, data_fim: datetime
    ) -> List[ContratacaoSchema]:
        query = (
            select(ContratacaoSchema)
            .options(
                selectinload(ContratacaoSchema.orgao_entidade),
                selectinload(ContratacaoSchema.unidade_orgao),
                selectinload(ContratacaoSchema.unidade_sub_rogada),
                selectinload(ContratacaoSchema.orgao_sub_rogado),
                selectinload(ContratacaoSchema.amparo_legal),
                selectinload(ContratacaoSchema.fontes_orcamentarias),
            )
            .where(
                ContratacaoSchema.data_atualizacao_global.between(data_ini, data_fim)
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def _get_by_id(self, entity_id: Any) -> Optional[ContratacaoSchema]:
        query = (
            select(ContratacaoSchema)
            .options(
                selectinload(ContratacaoSchema.orgao_entidade),
                selectinload(ContratacaoSchema.unidade_orgao),
                selectinload(ContratacaoSchema.unidade_sub_rogada),
                selectinload(ContratacaoSchema.orgao_sub_rogado),
                selectinload(ContratacaoSchema.amparo_legal),
                selectinload(ContratacaoSchema.fontes_orcamentarias),
            )
            .where(ContratacaoSchema.numero_controle_pncp == entity_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _upsert(
        self,
        entity: Contratacao,
        orgao_entidade_cnpj: Optional[str] = None,
        unidade_orgao_codigo_unidade: Optional[int] = None,
        amparo_legal_codigo: Optional[int] = None,
        unidade_sub_rogada_codigo_unidade: Optional[int] = None,
        orgao_sub_rogado_cnpj: Optional[str] = None,
    ) -> ContratacaoSchema:

        contratacao_existente = await self._get_by_id(entity.numero_controle_pncp)

        dados_contratacao = entity.model_dump(
            exclude={
                "orgao_entidade",
                "unidade_orgao",
                "amparo_legal",
                "unidade_sub_rogada",
                "orgao_sub_rogado",
                "fontes_orcamentarias",
            }
        )

        if orgao_entidade_cnpj is not None:
            dados_contratacao["orgao_entidade_cnpj"] = orgao_entidade_cnpj
        if unidade_orgao_codigo_unidade is not None:
            dados_contratacao["unidade_orgao_codigo_unidade"] = (
                unidade_orgao_codigo_unidade
            )
        if amparo_legal_codigo is not None:
            dados_contratacao["amparo_legal_codigo"] = amparo_legal_codigo
        if unidade_sub_rogada_codigo_unidade is not None:
            dados_contratacao["unidade_sub_rogada_codigo_unidade"] = (
                unidade_sub_rogada_codigo_unidade
            )
        if orgao_sub_rogado_cnpj is not None:
            dados_contratacao["orgao_sub_rogado_cnpj"] = orgao_sub_rogado_cnpj

        if contratacao_existente:
            for key, value in dados_contratacao.items():
                setattr(contratacao_existente, key, value)
            await self.session.commit()
            await self.session.refresh(contratacao_existente)
            return contratacao_existente
        else:
            contratacao_nova = ContratacaoSchema(**dados_contratacao)
            self.session.add(contratacao_nova)
            await self.session.commit()
            contratacao_nova = await self._get_by_id(entity.numero_controle_pncp)
            return contratacao_nova

    async def _list_all(
        self, limit: int = 100, offset: int = 0
    ) -> List[ContratacaoSchema]:

        query = (
            select(ContratacaoSchema)
            .options(
                selectinload(ContratacaoSchema.orgao_entidade),
                selectinload(ContratacaoSchema.unidade_orgao),
                selectinload(ContratacaoSchema.unidade_sub_rogada),
                selectinload(ContratacaoSchema.orgao_sub_rogado),
                selectinload(ContratacaoSchema.amparo_legal),
                selectinload(ContratacaoSchema.fontes_orcamentarias),
            )
            .order_by(ContratacaoSchema.numero_controle_pncp)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        db_results = result.scalars().all()
        return db_results
