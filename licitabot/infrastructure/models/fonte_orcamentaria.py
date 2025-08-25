from tortoise.models import Model
from tortoise import fields


class FonteOrcamentaria(Model):
    id = fields.IntField(pk=True)
    nome = fields.TextField(null=True)
    descricao = fields.TextField(null=True)
    data_inclusao = fields.DatetimeField(null=True)
    data_atualizacao = fields.DatetimeField(null=True)
    status_ativo = fields.BooleanField(null=True)

    class Meta:
        table = "fonte_orcamentaria"
