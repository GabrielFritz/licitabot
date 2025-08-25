from tortoise.models import Model
from tortoise import fields


class TipoMargemPreferencia(Model):
    codigo = fields.IntField(pk=True)
    nome = fields.TextField(null=True)

    class Meta:
        table = "tipo_margem_preferencia"
