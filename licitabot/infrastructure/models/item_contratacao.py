from tortoise.models import Model
from tortoise import fields


class ItemContratacao(Model):
    contratacao = fields.ForeignKeyField(
        "models.Contratacao", related_name="items", on_delete=fields.CASCADE
    )
    numero_controle_pncp = fields.TextField(null=True)
    item_id = fields.TextField(pk=True)
    numero_item = fields.IntField(null=True)
    descricao = fields.TextField(null=True)
    quantidade = fields.FloatField(null=True)
    unidade_medida = fields.TextField(null=True)
    material_ou_servico = fields.TextField(null=True)
    material_ou_servico_nome = fields.TextField(null=True)
    valor_unitario_estimado = fields.FloatField(null=True)
    valor_total = fields.FloatField(null=True)
    orcamento_sigiloso = fields.BooleanField(null=True)

    item_categoria_id = fields.IntField(null=True)
    item_categoria_nome = fields.TextField(null=True)
    criterio_julgamento_id = fields.IntField(null=True)
    criterio_julgamento_nome = fields.TextField(null=True)
    situacao_compra_item = fields.IntField(null=True)
    situacao_compra_item_nome = fields.TextField(null=True)
    tipo_beneficio = fields.IntField(null=True)
    tipo_beneficio_nome = fields.TextField(null=True)
    incentivo_produtivo_basico = fields.BooleanField(null=True)
    data_inclusao = fields.DatetimeField(null=True)
    data_atualizacao = fields.DatetimeField(null=True)
    tem_resultado = fields.BooleanField(null=True)
    aplicabilidade_margem_preferencia_normal = fields.BooleanField(null=True)
    aplicabilidade_margem_preferencia_adicional = fields.BooleanField(null=True)
    percentual_margem_preferencia_normal = fields.FloatField(null=True)
    percentual_margem_preferencia_adicional = fields.FloatField(null=True)
    ncm_nbs_codigo = fields.TextField(null=True)
    ncm_nbs_descricao = fields.TextField(null=True)
    catalogo = fields.ForeignKeyField(
        "models.Catalogo", related_name="items", on_delete=fields.RESTRICT, null=True
    )
    categoria_item_catalogo = fields.ForeignKeyField(
        "models.CategoriaItemCatalogo",
        related_name="items",
        on_delete=fields.RESTRICT,
        null=True,
    )
    catalogo_codigo_item = fields.TextField(null=True)
    informacao_complementar = fields.TextField(null=True)
    tipo_margem_preferencia = fields.ForeignKeyField(
        "models.TipoMargemPreferencia",
        related_name="items",
        on_delete=fields.RESTRICT,
        null=True,
    )
    exigencia_conteudo_nacional = fields.BooleanField(null=True)
    patrimonio = fields.TextField(null=True)
    codigo_registro_imobiliario = fields.TextField(null=True)
    imagem = fields.TextField(null=True)

    class Meta:
        table = "item_contratacao"
