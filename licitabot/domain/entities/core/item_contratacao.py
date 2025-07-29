from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, condecimal


class ItemContratacao(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    numero_controle_pncp: Optional[str] = None
    numero_item: int = Field(..., alias="numeroItem")
    descricao: str
    quantidade: float
    unidade_medida: str = Field(..., alias="unidadeMedida")

    material_ou_servico: str = Field(..., alias="materialOuServico")
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
    criterio_julgamento_id: int = Field(..., alias="criterioJulgamentoId")
    criterio_julgamento_nome: str = Field(..., alias="criterioJulgamentoNome")
    situacao_compra_item: int = Field(..., alias="situacaoCompraItem")
    situacao_compra_item_nome: str = Field(..., alias="situacaoCompraItemNome")

    tipo_beneficio: int = Field(..., alias="tipoBeneficio")
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
    catalogo: Optional[str] = Field(None, alias="catalogo")
    categoria_item_catalogo: Optional[str] = Field(None, alias="categoriaItemCatalogo")
    catalogo_codigo_item: Optional[str] = Field(None, alias="catalogoCodigoItem")

    informacao_complementar: Optional[str] = Field(None, alias="informacaoComplementar")
    tipo_margem_preferencia: Optional[str] = Field(None, alias="tipoMargemPreferencia")
    exigencia_conteudo_nacional: bool = Field(..., alias="exigenciaConteudoNacional")

    patrimonio: Optional[str] = None
    codigo_registro_imobiliario: Optional[str] = Field(
        None, alias="codigoRegistroImobiliario"
    )
    imagem: Optional[int] = None
