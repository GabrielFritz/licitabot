from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Annotated, Union

from pydantic import BaseModel, Field, PositiveInt, condecimal, field_validator

# ───────────────────────────────────────── Orgs / Unidades


class OrgaoEntidade(BaseModel):
    cnpj: str
    razao_social: str = Field(..., alias="razaoSocial")
    poder_id: str = Field(..., alias="poderId")
    esfera_id: str = Field(..., alias="esferaId")

    class Config:
        populate_by_name = True
        frozen = True


class UnidadeOrgao(BaseModel):
    codigo_unidade: str = Field(..., alias="codigoUnidade")
    nome_unidade: str = Field(..., alias="nomeUnidade")
    uf_sigla: str = Field(..., alias="ufSigla")
    municipio_nome: str = Field(..., alias="municipioNome")
    uf_nome: Optional[str] = Field(None, alias="ufNome")
    codigo_ibge: Optional[str] = Field(None, alias="codigoIbge")

    class Config:
        populate_by_name = True
        frozen = True


# ───────────────────────────────────────── Amparo legal / fonte


class AmparoLegal(BaseModel):
    codigo: PositiveInt
    nome: str
    descricao: str

    class Config:
        populate_by_name = True
        frozen = True


class FonteOrcamentaria(BaseModel):
    codigo: PositiveInt
    nome: str
    descricao: str
    data_inclusao: datetime = Field(..., alias="dataInclusao")

    class Config:
        populate_by_name = True
        frozen = True


# ───────────────────────────────────────── Contratação


class Contratacao(BaseModel):
    # IDs & chaves
    numero_controle_pncp: str = Field(..., alias="numeroControlePNCP")
    srp: bool

    # Órgão & unidade
    orgao_entidade: OrgaoEntidade = Field(..., alias="orgaoEntidade")
    unidade_orgao: UnidadeOrgao = Field(..., alias="unidadeOrgao")
    unidade_sub_rogada: Optional[UnidadeOrgao] = Field(None, alias="unidadeSubRogada")
    orgao_sub_rogado: Optional[OrgaoEntidade] = Field(None, alias="orgaoSubRogado")

    # Datas principais
    data_inclusao: datetime = Field(..., alias="dataInclusao")
    data_publicacao_pncp: datetime = Field(..., alias="dataPublicacaoPncp")
    data_atualizacao: datetime = Field(..., alias="dataAtualizacao")
    data_atualizacao_global: datetime = Field(..., alias="dataAtualizacaoGlobal")
    data_abertura_proposta: Optional[datetime] = Field(
        None, alias="dataAberturaProposta"
    )
    data_encerramento_proposta: Optional[datetime] = Field(
        None, alias="dataEncerramentoProposta"
    )

    # Identificação da compra
    ano_compra: int = Field(..., alias="anoCompra")
    sequencial_compra: int = Field(..., alias="sequencialCompra")
    numero_compra: str = Field(..., alias="numeroCompra")
    processo: str

    # Modalidade / disputa
    modalidade_id: int = Field(..., alias="modalidadeId")
    modalidade_nome: str = Field(..., alias="modalidadeNome")
    modo_disputa_id: Optional[int] = Field(None, alias="modoDisputaId")
    modo_disputa_nome: Optional[str] = Field(None, alias="modoDisputaNome")

    # Objeto e valores
    objeto_compra: str = Field(..., alias="objetoCompra")
    valor_total_estimado: Optional[
        Annotated[float, condecimal(max_digits=20, decimal_places=2)]
    ] = Field(None, alias="valorTotalEstimado")
    valor_total_homologado: Optional[
        Annotated[float, condecimal(max_digits=20, decimal_places=2)]
    ] = Field(None, alias="valorTotalHomologado")

    # Campo livre
    informacao_complementar: Optional[str] = Field(None, alias="informacaoComplementar")
    justificativa_presencial: Optional[str] = Field(
        None, alias="justificativaPresencial"
    )

    # Links
    link_sistema_origem: Optional[str] = Field(None, alias="linkSistemaOrigem")
    link_processo_eletronico: Optional[str] = Field(
        None, alias="linkProcessoEletronico"
    )

    # Situação
    situacao_compra_id: Union[str, int] = Field(
        ..., alias="situacaoCompraId"
    )  # às vezes string, às vezes int
    situacao_compra_nome: str = Field(..., alias="situacaoCompraNome")

    # Instrumento convocatório
    tipo_instrumento_convocatorio_codigo: Optional[int] = Field(
        None, alias="tipoInstrumentoConvocatorioCodigo"
    )
    tipo_instrumento_convocatorio_nome: Optional[str] = Field(
        None, alias="tipoInstrumentoConvocatorioNome"
    )

    # Amparo / fonte
    amparo_legal: AmparoLegal = Field(..., alias="amparoLegal")
    fontes_orcamentarias: List[FonteOrcamentaria] = Field(
        ..., alias="fontesOrcamentarias"
    )

    # Outros
    usuario_nome: str = Field(..., alias="usuarioNome")

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "numeroControlePNCP": "07854402000100-1-000054/2025",
                "srp": False,
                "orgaoEntidade": {
                    "cnpj": "07854402000100",
                    "razaoSocial": "EMPRESA MUNICIPAL DE AGUA E SANEAMENTO",
                    "poderId": "E",
                    "esferaId": "M",
                },
                "anoCompra": 2025,
                "sequencialCompra": 54,
                "dataInclusao": "2025-05-23T12:43:20",
                "dataAtualizacaoGlobal": "2025-07-11T00:00:44",
                "numeroCompra": "011/2025 - PE",
                "unidadeOrgao": {
                    "codigoUnidade": "15",
                    "nomeUnidade": "EMASA",
                    "ufSigla": "SC",
                    "municipioNome": "Balneário Camboriú",
                },
                "amparoLegal": {"codigo": 1, "nome": "...", "descricao": "..."},
                "objetoCompra": "REGISTRO DE PREÇOS ...",
                "modalidadeId": 6,
                "modalidadeNome": "Pregão - Eletrônico",
                "valorTotalEstimado": 89028.25,
                "situacaoCompraId": "1",
                "situacaoCompraNome": "Divulgada no PNCP",
                "usuarioNome": "PROCERGS",
                "fontesOrcamentarias": [],
            }
        }

    @field_validator("situacao_compra_id", mode="before")
    @classmethod
    def validate_situacao_compra_id(cls, v):
        """Convert situacaoCompraId to string if it's an integer."""
        if isinstance(v, int):
            return str(v)
        return v


# ───────────────────────────────────────── Item de contratacao


class ItemContratacao(BaseModel):
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

    # Categoria / julgamento
    item_categoria_id: int = Field(..., alias="itemCategoriaId")
    item_categoria_nome: str = Field(..., alias="itemCategoriaNome")
    criterio_julgamento_id: int = Field(..., alias="criterioJulgamentoId")
    criterio_julgamento_nome: str = Field(..., alias="criterioJulgamentoNome")
    situacao_compra_item: int = Field(..., alias="situacaoCompraItem")
    situacao_compra_item_nome: str = Field(..., alias="situacaoCompraItemNome")

    # Benefício / preferência
    tipo_beneficio: int = Field(..., alias="tipoBeneficio")
    tipo_beneficio_nome: str = Field(..., alias="tipoBeneficioNome")
    incentivo_produtivo_basico: bool = Field(..., alias="incentivoProdutivoBasico")

    # Datas
    data_inclusao: datetime = Field(..., alias="dataInclusao")
    data_atualizacao: datetime = Field(..., alias="dataAtualizacao")

    tem_resultado: bool = Field(..., alias="temResultado")

    # Preferência de margem
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

    # Catálogo / NCM
    ncm_nbs_codigo: Optional[str] = Field(None, alias="ncmNbsCodigo")
    ncm_nbs_descricao: Optional[str] = Field(None, alias="ncmNbsDescricao")
    catalogo: Optional[str]
    categoria_item_catalogo: Optional[str] = Field(None, alias="categoriaItemCatalogo")
    catalogo_codigo_item: Optional[str] = Field(None, alias="catalogoCodigoItem")

    # Complementos
    informacao_complementar: Optional[str] = Field(None, alias="informacaoComplementar")
    tipo_margem_preferencia: Optional[str] = Field(None, alias="tipoMargemPreferencia")
    exigencia_conteudo_nacional: bool = Field(..., alias="exigenciaConteudoNacional")

    # Outros campos
    patrimonio: Optional[str] = None
    codigo_registro_imobiliario: Optional[str] = Field(
        None, alias="codigoRegistroImobiliario"
    )
    imagem: Optional[int] = None

    class Config:
        populate_by_name = True
        from_attributes = True
