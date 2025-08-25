from tortoise.models import Model
from tortoise import fields


class Contratacao(Model):
    numero_controle_pncp = fields.TextField(pk=True)
    srp = fields.BooleanField(null=True)
    ano_compra = fields.IntField(null=True)
    sequencial_compra = fields.IntField(null=True)
    data_inclusao = fields.DatetimeField(null=True)
    data_publicacao_pncp = fields.DatetimeField(null=True)
    data_atualizacao = fields.DatetimeField(null=True)
    data_atualizacao_global = fields.DatetimeField(null=True)
    numero_compra = fields.TextField(null=True)
    data_abertura_proposta = fields.DatetimeField(null=True)
    data_encerramento_proposta = fields.DatetimeField(null=True)
    orgao_entidade = fields.ForeignKeyField(
        "models.OrgaoEntidade", related_name="contratacoes", null=True
    )
    unidade_orgao = fields.ForeignKeyField(
        "models.UnidadeOrgao", related_name="contratacoes", null=True
    )
    unidade_sub_rogada = fields.ForeignKeyField(
        "models.UnidadeOrgao", related_name="contratacoes_sub_rogadas", null=True
    )
    orgao_sub_rogado = fields.ForeignKeyField(
        "models.OrgaoEntidade", related_name="contratacoes_sub_rogadas", null=True
    )
    informacao_complementar = fields.TextField(null=True)
    processo = fields.TextField(null=True)
    objeto_compra = fields.TextField(null=True)
    link_sistema_origem = fields.TextField(null=True)
    link_processo_eletronico = fields.TextField(null=True)
    justificativa_presencial = fields.TextField(null=True)
    modalidade_id = fields.IntField(null=True)
    modalidade_nome = fields.TextField(null=True)
    modo_disputa_id = fields.IntField(null=True)
    modo_disputa_nome = fields.TextField(null=True)
    valor_total_estimado = fields.FloatField(null=True)
    valor_total_homologado = fields.FloatField(null=True)
    situacao_compra_id = fields.IntField(null=True)
    situacao_compra_nome = fields.TextField(null=True)
    tipo_instrumento_convocatorio_codigo = fields.IntField(null=True)
    tipo_instrumento_convocatorio_nome = fields.TextField(null=True)
    amparo_legal = fields.ForeignKeyField(
        "models.AmparoLegal", related_name="contratacoes", null=True
    )
    fontes_orcamentarias = fields.ManyToManyField(
        "models.FonteOrcamentaria", related_name="contratacoes", null=True
    )
    usuario_nome = fields.TextField(null=True)

    class Meta:
        table = "contratacao"
