"""
Testes para o serviço de persistência.
"""

import os
import sys
from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from unittest.mock import AsyncMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ingestor.services.persistence import (
    persist_contratacao_with_items,
    format_persistence_log,
    PersistenceResult,
)
from ingestor.models.pncp import (
    Contratacao,
    ItemContratacao,
    OrgaoEntidade,
    UnidadeOrgao,
    AmparoLegal,
)


class TestPersistenceResult(TestCase):
    """Testes para o modelo PersistenceResult."""

    def test_persistence_result_creation(self):
        """Testa criação de PersistenceResult."""
        result = PersistenceResult(
            success=True,
            numero_controle_pncp="07854402000100-1-000054/2025",
            itens_saved=5,
            orgao_upserted=True,
            unidade_upserted=True,
            amparo_upserted=True,
            fontes_upserted=2,
            duration_ms=245.5,
        )

        self.assertTrue(result.success)
        self.assertEqual(result.numero_controle_pncp, "07854402000100-1-000054/2025")
        self.assertEqual(result.itens_saved, 5)
        self.assertTrue(result.orgao_upserted)
        self.assertTrue(result.unidade_upserted)
        self.assertTrue(result.amparo_upserted)
        self.assertEqual(result.fontes_upserted, 2)
        self.assertEqual(result.duration_ms, 245.5)
        self.assertEqual(len(result.errors), 0)

    def test_add_error(self):
        """Testa adição de erro."""
        result = PersistenceResult(success=False)
        result.add_error("Erro de teste")

        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0], "Erro de teste")

    def test_is_success(self):
        """Testa verificação de sucesso."""
        # Sucesso sem erros
        result = PersistenceResult(success=True)
        self.assertTrue(result.is_success())

        # Sucesso com erros
        result = PersistenceResult(success=True)
        result.add_error("Erro")
        self.assertFalse(result.is_success())

        # Falha sem erros
        result = PersistenceResult(success=False)
        self.assertFalse(result.is_success())


class TestFormatPersistenceLog(TestCase):
    """Testes para formatação de logs de persistência."""

    def test_format_success_log(self):
        """Testa formatação de log de sucesso."""
        result = PersistenceResult(
            success=True,
            itens_saved=5,
            orgao_upserted=True,
            unidade_upserted=True,
            amparo_upserted=True,
            fontes_upserted=2,
            duration_ms=245.5,
        )

        log = format_persistence_log(result, "07854402000100-1-000054/2025")

        self.assertIn("✓", log)
        self.assertIn("5 itens salvos", log)
        self.assertIn("orgao:✓", log)
        self.assertIn("unidade:✓", log)
        self.assertIn("amparo:✓", log)
        self.assertIn("fontes:2", log)
        self.assertIn("duration:246ms", log)

    def test_format_error_log(self):
        """Testa formatação de log de erro."""
        result = PersistenceResult(success=False)
        result.add_error("CNPJ inválido")
        result.add_error("Timeout na conexão")

        log = format_persistence_log(result, "07854402000100-1-000055/2025")

        self.assertIn("❌", log)
        self.assertIn("Falha:", log)
        self.assertIn("CNPJ inválido; Timeout na conexão", log)

    def test_format_error_log_with_many_errors(self):
        """Testa formatação de log com muitos erros."""
        result = PersistenceResult(success=False)
        for i in range(5):
            result.add_error(f"Erro {i}")

        log = format_persistence_log(result, "07854402000100-1-000056/2025")

        self.assertIn("❌", log)
        self.assertIn("Erro 0; Erro 1 (+3 mais)", log)


class TestPersistenceService(TestCase):
    """Testes para o serviço de persistência."""

    def setUp(self):
        """Configura dados de teste."""
        # Cria dados de teste
        self.orgao = OrgaoEntidade(
            cnpj="07854402000100",
            razao_social="EMPRESA MUNICIPAL DE AGUA E SANEAMENTO",
            poder_id="E",
            esfera_id="M",
        )

        self.unidade = UnidadeOrgao(
            codigo_unidade="15",
            nome_unidade="EMASA",
            uf_sigla="SC",
            municipio_nome="Balneário Camboriú",
            uf_nome="Santa Catarina",
            codigo_ibge="4202008",
        )

        self.amparo = AmparoLegal(
            codigo=1, nome="Lei 8.666/93", descricao="Lei de Licitações e Contratos"
        )

        self.contratacao = Contratacao(
            numero_controle_pncp="07854402000100-1-000054/2025",
            srp=False,
            orgao_entidade=self.orgao,
            unidade_orgao=self.unidade,
            unidade_sub_rogada=None,
            orgao_sub_rogado=None,
            data_inclusao=datetime(2025, 1, 10, 14, 30, 0),
            data_publicacao_pncp=datetime(2025, 1, 10, 14, 30, 0),
            data_atualizacao=datetime(2025, 1, 10, 14, 30, 0),
            data_atualizacao_global=datetime(2025, 1, 10, 14, 30, 0),
            data_abertura_proposta=None,
            data_encerramento_proposta=None,
            ano_compra=2025,
            sequencial_compra=54,
            numero_compra="011/2025 - PE",
            processo="001/2025",
            modalidade_id=6,
            modalidade_nome="Pregão - Eletrônico",
            modo_disputa_id=None,
            modo_disputa_nome=None,
            objeto_compra="REGISTRO DE PREÇOS PARA AQUISIÇÃO DE MATERIAL DE CONSUMO",
            valor_total_estimado=89028.25,
            valor_total_homologado=None,
            informacao_complementar=None,
            justificativa_presencial=None,
            link_sistema_origem=None,
            link_processo_eletronico=None,
            situacao_compra_id="1",
            situacao_compra_nome="Divulgada no PNCP",
            tipo_instrumento_convocatorio_codigo=None,
            tipo_instrumento_convocatorio_nome=None,
            amparo_legal=self.amparo,
            fontes_orcamentarias=[],
            usuario_nome="PROCERGS",
        )

        self.item = ItemContratacao(
            numero_item=1,
            descricao="MATERIAL DE ESCRITÓRIO",
            quantidade=100.0,
            unidade_medida="UN",
            material_ou_servico="M",
            material_ou_servico_nome="Material",
            valor_unitario_estimado=10.50,
            valor_total=1050.00,
            orcamento_sigiloso=False,
            item_categoria_id=1,
            item_categoria_nome="Material de Consumo",
            criterio_julgamento_id=1,
            criterio_julgamento_nome="Menor Preço",
            situacao_compra_item=1,
            situacao_compra_item_nome="Ativo",
            tipo_beneficio=1,
            tipo_beneficio_nome="Nenhum",
            incentivo_produtivo_basico=False,
            data_inclusao=datetime(2025, 1, 10, 14, 30, 0),
            data_atualizacao=datetime(2025, 1, 10, 14, 30, 0),
            tem_resultado=False,
            aplicabilidade_margem_preferencia_normal=False,
            aplicabilidade_margem_preferencia_adicional=False,
            percentual_margem_preferencia_normal=None,
            percentual_margem_preferencia_adicional=None,
            ncm_nbs_codigo=None,
            ncm_nbs_descricao=None,
            catalogo=None,
            categoria_item_catalogo=None,
            catalogo_codigo_item=None,
            informacao_complementar=None,
            tipo_margem_preferencia=None,
            exigencia_conteudo_nacional=False,
            patrimonio=None,
            codigo_registro_imobiliario=None,
            imagem=None,
        )

    @patch("ingestor.services.persistence.get_async_session")
    async def test_persist_contratacao_with_items_success(self, mock_session):
        """Testa persistência bem-sucedida."""
        # Mock da sessão
        mock_session.return_value.__aenter__.return_value = AsyncMock()

        # Mock dos repositórios
        with patch(
            "ingestor.services.persistence.OrgaoRepository"
        ) as mock_orgao_repo, patch(
            "ingestor.services.persistence.UnidadeRepository"
        ) as mock_unidade_repo, patch(
            "ingestor.services.persistence.ContratacaoRepository"
        ) as mock_contratacao_repo, patch(
            "ingestor.services.persistence.ItemRepository"
        ) as mock_item_repo:

            # Configura mocks
            mock_orgao_repo.return_value.upsert.return_value = AsyncMock(id=1)
            mock_unidade_repo.return_value.upsert.return_value = AsyncMock(id=2)
            mock_contratacao_repo.return_value.upsert_amparo_legal.return_value = (
                AsyncMock(id=3)
            )
            mock_contratacao_repo.return_value.upsert.return_value = AsyncMock(
                numero_controle_pncp="07854402000100-1-000054/2025"
            )
            mock_item_repo.return_value.upsert_batch.return_value = [
                AsyncMock() for _ in range(1)
            ]

            # Executa persistência
            result = await persist_contratacao_with_items(self.contratacao, [self.item])

            # Verifica resultado
            self.assertTrue(result.success)
            self.assertEqual(
                result.numero_controle_pncp, "07854402000100-1-000054/2025"
            )
            self.assertEqual(result.itens_saved, 1)
            self.assertTrue(result.orgao_upserted)
            self.assertTrue(result.unidade_upserted)
            self.assertTrue(result.amparo_upserted)
            self.assertEqual(result.fontes_upserted, 0)
            self.assertEqual(len(result.errors), 0)

    @patch("ingestor.services.persistence.get_async_session")
    async def test_persist_contratacao_with_items_error(self, mock_session):
        """Testa persistência com erro."""
        # Mock da sessão
        mock_session.return_value.__aenter__.return_value = AsyncMock()

        # Mock dos repositórios com erro
        with patch("ingestor.services.persistence.OrgaoRepository") as mock_orgao_repo:
            mock_orgao_repo.return_value.upsert.side_effect = Exception("Erro de teste")

            # Executa persistência
            result = await persist_contratacao_with_items(self.contratacao, [self.item])

            # Verifica resultado
            self.assertFalse(result.success)
            self.assertEqual(len(result.errors), 1)
            self.assertIn("Erro ao salvar órgão", result.errors[0])


if __name__ == "__main__":
    import unittest
    import asyncio

    # Executa testes assíncronos
    async def run_async_tests():
        unittest.main()

    asyncio.run(run_async_tests())
