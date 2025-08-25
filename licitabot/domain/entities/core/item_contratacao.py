from datetime import datetime
from typing import Annotated, Optional
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, condecimal
from licitabot.domain.entities.core.catalogo import Catalogo
from licitabot.domain.entities.core.categoria_item_catalogo import CategoriaItemCatalogo
from licitabot.domain.entities.core.tipo_margem_preferencia import TipoMargemPreferencia


class MaterialOuServico(Enum):
    MATERIAL = "M"
    SERVICO = "S"


class CriterioJulgamentoId(Enum):
    MENOR_PRECO = 1
    MAIOR_DESCONTO = 2
    TECNICA_E_PRECO = 3
    MAIOR_LANCE = 4
    MAIOR_RETORNO_ECONOMICO = 5
    NAO_APLICAVEL = 6


class SituacaoCompraItem(Enum):
    EM_ANDAMENTO = 1
    HOMOLOGADO = 2
    CANCELADO = 3
    DESERTO = 4
    FRACASSADO = 5


class TipoBeneficio(Enum):
    EXCLUSIVO_ME_EPP = 1
    SUBCONTRATACAO_ME_EPP = 2
    COTA_RESERVADA_ME_EPP = 3
    SEM_BENEFICIO = 4
    NAO_APLICAVEL = 5


class ItemContratacao(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    numero_controle_pncp: Optional[str] = Field(None, alias="numeroControlePncp")
    item_id: str = Field(..., alias="item_id")
    numero_item: int = Field(..., alias="numeroItem")
    descricao: str
    quantidade: float
    unidade_medida: str = Field(..., alias="unidadeMedida")

    material_ou_servico: MaterialOuServico = Field(..., alias="materialOuServico")
    material_ou_servico_nome: str = Field(..., alias="materialOuServicoNome")

    valor_unitario_estimado: Optional[
        Annotated[float, condecimal(max_digits=20, decimal_places=2)]
    ] = Field(None, alias="valorUnitarioEstimado")
    valor_total: Optional[
        Annotated[float, condecimal(max_digits=20, decimal_places=2)]
    ] = Field(None, alias="valorTotal")

    orcamento_sigiloso: bool = Field(..., alias="orcamentoSigiloso")

    item_categoria_id: int = Field(..., alias="itemCategoriaId")
    item_categoria_nome: str = Field(..., alias="itemCategoriaNome")
    criterio_julgamento_id: CriterioJulgamentoId = Field(
        ..., alias="criterioJulgamentoId"
    )
    criterio_julgamento_nome: str = Field(..., alias="criterioJulgamentoNome")
    situacao_compra_item: SituacaoCompraItem = Field(..., alias="situacaoCompraItem")
    situacao_compra_item_nome: str = Field(..., alias="situacaoCompraItemNome")

    tipo_beneficio: TipoBeneficio = Field(..., alias="tipoBeneficio")
    tipo_beneficio_nome: str = Field(..., alias="tipoBeneficioNome")
    incentivo_produtivo_basico: bool = Field(..., alias="incentivoProdutivoBasico")

    data_inclusao: datetime = Field(..., alias="dataInclusao")
    data_atualizacao: datetime = Field(..., alias="dataAtualizacao")

    tem_resultado: bool = Field(..., alias="temResultado")

    aplicabilidade_margem_preferencia_normal: bool = Field(
        ..., alias="aplicabilidadeMargemPreferenciaNormal"
    )
    aplicabilidade_margem_preferencia_adicional: bool = Field(
        ..., alias="aplicabilidadeMargemPreferenciaAdicional"
    )
    percentual_margem_preferencia_normal: Optional[float] = Field(
        None, alias="percentualMargemPreferenciaNormal"
    )
    percentual_margem_preferencia_adicional: Optional[float] = Field(
        None, alias="percentualMargemPreferenciaAdicional"
    )

    ncm_nbs_codigo: Optional[str] = Field(None, alias="ncmNbsCodigo")
    ncm_nbs_descricao: Optional[str] = Field(None, alias="ncmNbsDescricao")
    catalogo: Optional[Catalogo] = Field(None, alias="catalogo")
    categoria_item_catalogo: Optional[CategoriaItemCatalogo] = Field(
        None, alias="categoriaItemCatalogo"
    )
    catalogo_codigo_item: Optional[str] = Field(None, alias="catalogoCodigoItem")

    informacao_complementar: Optional[str] = Field(None, alias="informacaoComplementar")
    tipo_margem_preferencia: Optional[TipoMargemPreferencia] = Field(
        None, alias="tipoMargemPreferencia"
    )
    exigencia_conteudo_nacional: bool = Field(..., alias="exigenciaConteudoNacional")

    patrimonio: Optional[str] = None
    codigo_registro_imobiliario: Optional[str] = Field(
        None, alias="codigoRegistroImobiliario"
    )
    imagem: Optional[int] = None
