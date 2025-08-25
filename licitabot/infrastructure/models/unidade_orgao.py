from tortoise.models import Model
from tortoise import fields


class UnidadeOrgao(Model):
    codigo_unidade = fields.TextField(pk=True)
    nome_unidade = fields.TextField(null=True)
    uf_sigla = fields.TextField(null=True)
    municipio_nome = fields.TextField(null=True)
    uf_nome = fields.TextField(null=True)
    codigo_ibge = fields.TextField(null=True)

    class Meta:
        table = "unidade_orgao"
