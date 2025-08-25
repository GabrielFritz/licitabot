import re
from enum import Enum


class YearMonthDay(str):

    PATTERN = re.compile(r"^(\d{4})(\d{2})(\d{2})$")

    def __new__(cls, value: str):
        if not cls.is_valid_format(value):
            raise ValueError(f"Invalid YearMonthDay format: {value}")
        return str.__new__(cls, value)

    @classmethod
    def is_valid_format(cls, value: str) -> bool:
        return bool(cls.PATTERN.match(value))

    @classmethod
    def from_string(cls, value: str) -> "YearMonthDay":
        if cls.is_valid_format(value):
            return cls(value)
        raise ValueError(f"Invalid YearMonthDay format: {value}")


class SituacaoCompraId(Enum):
    DIVULGADA_NO_PNCP = 1
    REVOGADA = 2
    ANULADA = 3
    SUSPENSA = 4


class ModalidadeId(Enum):
    LEILAO_ELETRONICO = 1
    DIALOGO_COMPETITIVO = 2
    CONCURSO = 3
    CONCORRENCIA_ELETRONICA = 4
    CONCORRENCIA_PRESENCIAL = 5
    PREGAO_ELETRONICO = 6
    PREGAO_PRESENCIAL = 7
    DISPENSA = 8
    INEXIGIBILIDADE = 9
    MANIFESTACAO_DE_INTERESSE = 10
    PRE_QUALIFICACAO = 11
    CREDENCIAMENTO = 12
    LEILAO_PRESENCIAL = 13


class ModoDisputaId(Enum):
    ABERTO = 1
    FECHADO = 2
    ABERTO_E_FECHADO = 3
    DISPENSA_COM_DISPUTA = 4
    NAO_APLICAVEL = 5
    FECHADO_E_ABERTO = 6


class InstrumentoConvocatorioCodigo(Enum):
    EDITAL = 1
    AVISO_CONTRATACAO_DIRETA = 2
    ATO_AUTORIZACAO_CONTRATACAO_DIRETA = 3
