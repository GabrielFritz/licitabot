from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, Field, condecimal, field_validator

from licitabot.domain.entities.core.amparo_legal import AmparoLegal
from licitabot.domain.entities.core.fonte_orcamentaria import FonteOrcamentaria
from licitabot.domain.entities.core.orgao_entidade import OrgaoEntidade
from licitabot.domain.entities.core.unidade_orgao import UnidadeOrgao


class Contratacao(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
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
                "situacaoCompraId": 1,
                "situacaoCompraNome": "Divulgada no PNCP",
                "usuarioNome": "PROCERGS",
                "fontesOrcamentarias": [],
            }
        },
    )

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
    situacao_compra_id: int = Field(..., alias="situacaoCompraId")
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

    @field_validator("situacao_compra_id", mode="before")
    @classmethod
    def validate_situacao_compra_id(cls, v):
        """Convert situacaoCompraId to string if it's an integer."""
        if isinstance(v, int):
            return str(v)
        return v
