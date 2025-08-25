from licitabot.domain.entities import (
    AmparoLegal,
    Catalogo,
    CategoriaItemCatalogo,
    FonteOrcamentaria,
    ItemContratacao,
    OrgaoEntidade,
    TipoMargemPreferencia,
    UnidadeOrgao,
)
from licitabot.infrastructure.models.amparo_legal import (
    AmparoLegal as AmparoLegalSchema,
)
from licitabot.infrastructure.models import (
    Catalogo as CatalogoSchema,
    CategoriaItemCatalogo as CategoriaItemCatalogoSchema,
    FonteOrcamentaria as FonteOrcamentariaSchema,
    ItemContratacao as ItemContratacaoSchema,
    OrgaoEntidade as OrgaoEntidadeSchema,
    TipoMargemPreferencia as TipoMargemPreferenciaSchema,
    UnidadeOrgao as UnidadeOrgaoSchema,
)
from licitabot.infrastructure.repositories.base_repository import BaseRepository


class AmparoLegalRepository(BaseRepository[AmparoLegal, AmparoLegalSchema]):
    pydantic_model = AmparoLegal
    tortoise_model = AmparoLegalSchema
    pk_field = "codigo"


class CatalogoRepository(BaseRepository[Catalogo, CatalogoSchema]):
    pydantic_model = Catalogo
    tortoise_model = CatalogoSchema
    pk_field = "id"


class CategoriaItemCatalogoRepository(
    BaseRepository[CategoriaItemCatalogo, CategoriaItemCatalogoSchema]
):
    pydantic_model = CategoriaItemCatalogo
    tortoise_model = CategoriaItemCatalogoSchema
    pk_field = "id"


class FonteOrcamentariaRepository(
    BaseRepository[FonteOrcamentaria, FonteOrcamentariaSchema]
):
    pydantic_model = FonteOrcamentaria
    tortoise_model = FonteOrcamentariaSchema
    pk_field = "id"


class OrgaoEntidadeRepository(BaseRepository[OrgaoEntidade, OrgaoEntidadeSchema]):
    pydantic_model = OrgaoEntidade
    tortoise_model = OrgaoEntidadeSchema
    pk_field = "cnpj"


class TipoMargemPreferenciaRepository(
    BaseRepository[TipoMargemPreferencia, TipoMargemPreferenciaSchema]
):
    pydantic_model = TipoMargemPreferencia
    tortoise_model = TipoMargemPreferenciaSchema
    pk_field = "codigo"


class UnidadeOrgaoRepository(BaseRepository[UnidadeOrgao, UnidadeOrgaoSchema]):
    pydantic_model = UnidadeOrgao
    tortoise_model = UnidadeOrgaoSchema
    pk_field = "codigo_unidade"
