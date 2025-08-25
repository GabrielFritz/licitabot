from datetime import datetime
from typing import Annotated, List, Optional
import re

from pydantic import BaseModel, ConfigDict, Field, condecimal, field_validator

from licitabot.domain.entities.core.amparo_legal import AmparoLegal
from licitabot.domain.entities.core.fonte_orcamentaria import FonteOrcamentaria
from licitabot.domain.entities.core.orgao_entidade import OrgaoEntidade
from licitabot.domain.entities.core.unidade_orgao import UnidadeOrgao
from licitabot.domain.entities.core.item_contratacao import ItemContratacao
from licitabot.domain.entities.core.value_objects import (
    ModalidadeId,
    ModoDisputaId,
    SituacaoCompraId,
    InstrumentoConvocatorioCodigo,
)


class NumeroControlePNCP(str):

    PATTERN = re.compile(r"^(\d{14})-(\d+)-(\d{6})/(\d{4})$")

    def __new__(cls, value: str):
        if not cls.is_valid_format(value):
            raise ValueError(
                f"Invalid NumeroControlePNCP format: {value}. Expected format: CNPJ-TIPO-SEQUENCIAL/ANO"
            )
        return str.__new__(cls, value)

    @classmethod
    def is_valid_format(cls, value: str) -> bool:
        return bool(cls.PATTERN.match(value))

    @classmethod
    def from_string(cls, value: str) -> "NumeroControlePNCP":
        if cls.is_valid_format(value):
            return cls(value)
        raise ValueError(f"Invalid NumeroControlePNCP format: {value}")

    def parse_components(self) -> dict:
        match = self.PATTERN.match(self)
        if match:
            return {
                "cnpj": match.group(1),
                "tipo": match.group(2),
                "sequencial": match.group(3),
                "ano": match.group(4),
            }
        return {}

    @property
    def cnpj(self) -> str:
        return self.parse_components().get("cnpj", "")

    @property
    def ano(self) -> str:
        return self.parse_components().get("ano", "")

    @property
    def sequencial(self) -> str:
        return self.parse_components().get("sequencial", "")


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

    numero_controle_pncp: NumeroControlePNCP = Field(..., alias="numeroControlePNCP")
    srp: bool = Field(..., alias="srp")
    ano_compra: int = Field(..., alias="anoCompra")
    sequencial_compra: int = Field(..., alias="sequencialCompra")
    data_inclusao: datetime = Field(..., alias="dataInclusao")
    data_publicacao_pncp: datetime = Field(..., alias="dataPublicacaoPncp")
    data_atualizacao: datetime = Field(..., alias="dataAtualizacao")
    data_atualizacao_global: datetime = Field(..., alias="dataAtualizacaoGlobal")
    numero_compra: str = Field(..., alias="numeroCompra")
    data_abertura_proposta: Optional[datetime] = Field(
        None, alias="dataAberturaProposta"
    )
    data_encerramento_proposta: Optional[datetime] = Field(
        None, alias="dataEncerramentoProposta"
    )
    orgao_entidade: OrgaoEntidade = Field(..., alias="orgaoEntidade")
    unidade_orgao: UnidadeOrgao = Field(..., alias="unidadeOrgao")
    unidade_sub_rogada: Optional[UnidadeOrgao] = Field(None, alias="unidadeSubRogada")
    orgao_sub_rogado: Optional[OrgaoEntidade] = Field(None, alias="orgaoSubRogado")
    informacao_complementar: Optional[str] = Field(None, alias="informacaoComplementar")
    processo: str = Field(..., alias="processo")
    objeto_compra: str = Field(..., alias="objetoCompra")
    link_sistema_origem: Optional[str] = Field(None, alias="linkSistemaOrigem")
    link_processo_eletronico: Optional[str] = Field(
        None, alias="linkProcessoEletronico"
    )
    justificativa_presencial: Optional[str] = Field(
        None, alias="justificativaPresencial"
    )
    modalidade_id: ModalidadeId = Field(..., alias="modalidadeId")
    modalidade_nome: str = Field(..., alias="modalidadeNome")
    modo_disputa_id: Optional[ModoDisputaId] = Field(None, alias="modoDisputaId")
    modo_disputa_nome: Optional[str] = Field(None, alias="modoDisputaNome")
    valor_total_estimado: Optional[
        Annotated[float, condecimal(max_digits=20, decimal_places=2)]
    ] = Field(None, alias="valorTotalEstimado")
    valor_total_homologado: Optional[
        Annotated[float, condecimal(max_digits=20, decimal_places=2)]
    ] = Field(None, alias="valorTotalHomologado")
    situacao_compra_id: SituacaoCompraId = Field(..., alias="situacaoCompraId")
    situacao_compra_nome: str = Field(..., alias="situacaoCompraNome")
    tipo_instrumento_convocatorio_codigo: Optional[InstrumentoConvocatorioCodigo] = (
        Field(None, alias="tipoInstrumentoConvocatorioCodigo")
    )
    tipo_instrumento_convocatorio_nome: Optional[str] = Field(
        None, alias="tipoInstrumentoConvocatorioNome"
    )
    amparo_legal: AmparoLegal = Field(..., alias="amparoLegal")
    fontes_orcamentarias: List[FonteOrcamentaria] = Field(
        ..., alias="fontesOrcamentarias"
    )
    usuario_nome: str = Field(..., alias="usuarioNome")

    items: List[ItemContratacao] = Field(default_factory=list, alias="items")

    @field_validator("numero_controle_pncp", mode="before")
    @classmethod
    def validate_numero_controle_pncp(cls, v):
        if isinstance(v, str) and NumeroControlePNCP.is_valid_format(v):
            return NumeroControlePNCP(v)
        return v
