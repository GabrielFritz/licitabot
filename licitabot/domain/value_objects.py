import re
from datetime import datetime


class NumeroPagina(int):
    def __new__(cls, value: int):
        if value < 1:
            raise ValueError(f"Invalid NumeroPagina: {value}")
        return int.__new__(cls, value)


class TamanhoPagina(int):
    def __new__(cls, value: int):
        if value not in [10, 50]:
            raise ValueError(f"Invalid TamanhoPagina: {value}")
        return int.__new__(cls, value)


class TotalPaginas(int):
    def __new__(cls, value: int):
        if value <= 1:
            raise ValueError(f"Invalid TotalPaginas: {value}")
        return int.__new__(cls, value)


class YearMonthDay(str):
    PATTERN = re.compile(r"^\d{4}\d{2}\d{2}$")

    def __new__(cls, value: str):
        if not cls.PATTERN.match(value):
            raise ValueError(f"Invalid YearMonthDay format: {value}")
        return str.__new__(cls, value)


class CodigoModalidadeContratacao(int):

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

    def __new__(cls, value: int):
        if value not in [
            cls.LEILAO_ELETRONICO,
            cls.DIALOGO_COMPETITIVO,
            cls.CONCURSO,
            cls.CONCORRENCIA_ELETRONICA,
            cls.CONCORRENCIA_PRESENCIAL,
            cls.PREGAO_ELETRONICO,
            cls.PREGAO_PRESENCIAL,
            cls.DISPENSA,
            cls.INEXIGIBILIDADE,
            cls.MANIFESTACAO_DE_INTERESSE,
            cls.PRE_QUALIFICACAO,
            cls.CREDENCIAMENTO,
            cls.LEILAO_PRESENCIAL,
        ]:
            raise ValueError(f"Invalid codigoModalidadeContratacao: {value}")
        return int.__new__(cls, value)


class NumeroControlePNCP(str):
    PATTERN = re.compile(r"^\d{14}-\d{1}-\d{6}/\d{4}$")

    def __new__(cls, value: str):
        if not cls.PATTERN.match(value):
            raise ValueError(f"Invalid NumeroControlePNCP format: {value}")
        return str.__new__(cls, value)


class CNPJ(str):
    PATTERN = re.compile(r"^\d{14}$")

    def __new__(cls, value: str):
        if not cls.PATTERN.match(value):
            raise ValueError(f"Invalid CNPJ format: {value}")
        return str.__new__(cls, value)


class Ano(int):
    def __new__(cls, value: int):
        if value < 1900:
            raise ValueError(f"Invalid Ano: {value}")
        return int.__new__(cls, value)


class Sequencial(int):
    def __new__(cls, value: int):
        if value < 1:
            raise ValueError(f"Invalid Sequencial: {value}")
        return int.__new__(cls, value)


class IngestionWindow:
    def __init__(self, data_inicial: YearMonthDay, data_final: YearMonthDay):
        self._validate_ingestion_window(data_inicial, data_final)
        self.data_inicial = data_inicial
        self.data_final = data_final

    @classmethod
    def from_datetime(cls, data_inicial: datetime, data_final: datetime):
        return cls(
            YearMonthDay(data_inicial.strftime("%Y%m%d")),
            YearMonthDay(data_final.strftime("%Y%m%d")),
        )

    def _validate_ingestion_window(
        self, data_inicial: YearMonthDay, data_final: YearMonthDay
    ):
        if data_inicial > data_final:
            raise ValueError(f"Invalid ingestion window: {data_inicial} > {data_final}")
