from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "amparo_legal" (
    "codigo" SERIAL NOT NULL PRIMARY KEY,
    "nome" TEXT,
    "descricao" TEXT
);
CREATE TABLE IF NOT EXISTS "catalogo" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nome" TEXT,
    "descricao" TEXT,
    "data_inclusao" TIMESTAMPTZ,
    "data_atualizacao" TIMESTAMPTZ,
    "status_ativo" BOOL,
    "url" TEXT
);
CREATE TABLE IF NOT EXISTS "categoria_item_catalogo" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nome" TEXT,
    "descricao" TEXT,
    "data_inclusao" TIMESTAMPTZ,
    "data_atualizacao" TIMESTAMPTZ,
    "status_ativo" BOOL
);
CREATE TABLE IF NOT EXISTS "fonte_orcamentaria" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nome" TEXT,
    "descricao" TEXT,
    "data_inclusao" TIMESTAMPTZ,
    "data_atualizacao" TIMESTAMPTZ,
    "status_ativo" BOOL
);
CREATE TABLE IF NOT EXISTS "orgao_entidade" (
    "cnpj" TEXT NOT NULL PRIMARY KEY,
    "razao_social" TEXT,
    "poder_id" TEXT,
    "esfera_id" TEXT
);
CREATE TABLE IF NOT EXISTS "tipo_margem_preferencia" (
    "codigo" SERIAL NOT NULL PRIMARY KEY,
    "nome" TEXT
);
CREATE TABLE IF NOT EXISTS "unidade_orgao" (
    "codigo_unidade" TEXT NOT NULL PRIMARY KEY,
    "nome_unidade" TEXT,
    "uf_sigla" TEXT,
    "municipio_nome" TEXT,
    "uf_nome" TEXT,
    "codigo_ibge" TEXT
);
CREATE TABLE IF NOT EXISTS "contratacao" (
    "numero_controle_pncp" TEXT NOT NULL PRIMARY KEY,
    "srp" BOOL,
    "ano_compra" INT,
    "sequencial_compra" INT,
    "data_inclusao" TIMESTAMPTZ,
    "data_publicacao_pncp" TIMESTAMPTZ,
    "data_atualizacao" TIMESTAMPTZ,
    "data_atualizacao_global" TIMESTAMPTZ,
    "numero_compra" TEXT,
    "data_abertura_proposta" TIMESTAMPTZ,
    "data_encerramento_proposta" TIMESTAMPTZ,
    "informacao_complementar" TEXT,
    "processo" TEXT,
    "objeto_compra" TEXT,
    "link_sistema_origem" TEXT,
    "link_processo_eletronico" TEXT,
    "justificativa_presencial" TEXT,
    "modalidade_id" INT,
    "modalidade_nome" TEXT,
    "modo_disputa_id" INT,
    "modo_disputa_nome" TEXT,
    "valor_total_estimado" DOUBLE PRECISION,
    "valor_total_homologado" DOUBLE PRECISION,
    "situacao_compra_id" INT,
    "situacao_compra_nome" TEXT,
    "tipo_instrumento_convocatorio_codigo" INT,
    "tipo_instrumento_convocatorio_nome" TEXT,
    "usuario_nome" TEXT,
    "amparo_legal_id" INT REFERENCES "amparo_legal" ("codigo") ON DELETE CASCADE,
    "orgao_entidade_id" TEXT REFERENCES "orgao_entidade" ("cnpj") ON DELETE CASCADE,
    "orgao_sub_rogado_id" TEXT REFERENCES "orgao_entidade" ("cnpj") ON DELETE CASCADE,
    "unidade_orgao_id" TEXT REFERENCES "unidade_orgao" ("codigo_unidade") ON DELETE CASCADE,
    "unidade_sub_rogada_id" TEXT REFERENCES "unidade_orgao" ("codigo_unidade") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "item_contratacao" (
    "numero_controle_pncp" TEXT,
    "item_id" TEXT NOT NULL PRIMARY KEY,
    "numero_item" INT,
    "descricao" TEXT,
    "quantidade" DOUBLE PRECISION,
    "unidade_medida" TEXT,
    "material_ou_servico" TEXT,
    "material_ou_servico_nome" TEXT,
    "valor_unitario_estimado" DOUBLE PRECISION,
    "valor_total" DOUBLE PRECISION,
    "orcamento_sigiloso" BOOL,
    "item_categoria_id" INT,
    "item_categoria_nome" TEXT,
    "criterio_julgamento_id" INT,
    "criterio_julgamento_nome" TEXT,
    "situacao_compra_item" INT,
    "situacao_compra_item_nome" TEXT,
    "tipo_beneficio" INT,
    "tipo_beneficio_nome" TEXT,
    "incentivo_produtivo_basico" BOOL,
    "data_inclusao" TIMESTAMPTZ,
    "data_atualizacao" TIMESTAMPTZ,
    "tem_resultado" BOOL,
    "aplicabilidade_margem_preferencia_normal" BOOL,
    "aplicabilidade_margem_preferencia_adicional" BOOL,
    "percentual_margem_preferencia_normal" DOUBLE PRECISION,
    "percentual_margem_preferencia_adicional" DOUBLE PRECISION,
    "ncm_nbs_codigo" TEXT,
    "ncm_nbs_descricao" TEXT,
    "catalogo_codigo_item" TEXT,
    "informacao_complementar" TEXT,
    "exigencia_conteudo_nacional" BOOL,
    "patrimonio" TEXT,
    "codigo_registro_imobiliario" TEXT,
    "imagem" TEXT,
    "catalogo_id" INT REFERENCES "catalogo" ("id") ON DELETE RESTRICT,
    "categoria_item_catalogo_id" INT REFERENCES "categoria_item_catalogo" ("id") ON DELETE RESTRICT,
    "contratacao_id" TEXT NOT NULL REFERENCES "contratacao" ("numero_controle_pncp") ON DELETE CASCADE,
    "tipo_margem_preferencia_id" INT REFERENCES "tipo_margem_preferencia" ("codigo") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "contratacao_fonte_orcamentaria" (
    "contratacao_id" TEXT NOT NULL REFERENCES "contratacao" ("numero_controle_pncp") ON DELETE CASCADE,
    "fonteorcamentaria_id" INT NOT NULL REFERENCES "fonte_orcamentaria" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_contratacao_contrat_dee689" ON "contratacao_fonte_orcamentaria" ("contratacao_id", "fonteorcamentaria_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
