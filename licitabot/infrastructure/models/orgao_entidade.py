from tortoise.models import Model
from tortoise import fields


class OrgaoEntidade(Model):
    cnpj = fields.TextField(pk=True)
    razao_social = fields.TextField(null=True)
    poder_id = fields.TextField(null=True)
    esfera_id = fields.TextField(null=True)

    class Meta:
        table = "orgao_entidade"
