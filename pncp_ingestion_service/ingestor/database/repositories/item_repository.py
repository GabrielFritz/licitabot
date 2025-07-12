"""
Repositório para operações com itens de contratação.
"""

from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ingestor.database.models import ItemContratacao
from ingestor.models.pncp import ItemContratacao as ItemContratacaoPydantic


class ItemRepository:
    """Repositório para operações com itens de contratação."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_contratacao_and_numero(
        self, numero_controle_pncp: str, numero_item: int
    ) -> Optional[ItemContratacao]:
        """
        Busca item por contratação e número do item.

        Args:
            numero_controle_pncp: Número de controle da contratação
            numero_item: Número do item

        Returns:
            ItemContratacao ou None se não encontrado
        """
        stmt = select(ItemContratacao).where(
            ItemContratacao.numero_controle_pncp == numero_controle_pncp,
            ItemContratacao.numero_item == numero_item,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_by_contratacao(self, numero_controle_pncp: str) -> int:
        """
        Remove todos os itens de uma contratação.

        Args:
            numero_controle_pncp: Número de controle da contratação

        Returns:
            Número de itens removidos
        """
        stmt = delete(ItemContratacao).where(
            ItemContratacao.numero_controle_pncp == numero_controle_pncp
        )
        result = await self.session.execute(stmt)
        return result.rowcount

    async def upsert_batch(
        self, itens_pydantic: List[ItemContratacaoPydantic], numero_controle_pncp: str
    ) -> List[ItemContratacao]:
        """
        Upsert lote de itens.

        Args:
            itens_pydantic: Lista de itens vindos da API
            numero_controle_pncp: Número de controle da contratação

        Returns:
            Lista de ItemContratacao salvos/atualizados
        """
        itens_salvos = []

        for item_pydantic in itens_pydantic:
            # Dados do item
            dados_item = {
                "numero_controle_pncp": numero_controle_pncp,
                "numero_item": item_pydantic.numero_item,
                "descricao": item_pydantic.descricao,
                "quantidade": item_pydantic.quantidade,
                "unidade_medida": item_pydantic.unidade_medida,
                "material_ou_servico": item_pydantic.material_ou_servico,
                "material_ou_servico_nome": item_pydantic.material_ou_servico_nome,
                "valor_unitario_estimado": item_pydantic.valor_unitario_estimado,
                "valor_total": item_pydantic.valor_total,
                "orcamento_sigiloso": item_pydantic.orcamento_sigiloso,
                "item_categoria_id": item_pydantic.item_categoria_id,
                "item_categoria_nome": item_pydantic.item_categoria_nome,
                "criterio_julgamento_id": item_pydantic.criterio_julgamento_id,
                "criterio_julgamento_nome": item_pydantic.criterio_julgamento_nome,
                "situacao_compra_item": item_pydantic.situacao_compra_item,
                "situacao_compra_item_nome": item_pydantic.situacao_compra_item_nome,
                "tipo_beneficio": item_pydantic.tipo_beneficio,
                "tipo_beneficio_nome": item_pydantic.tipo_beneficio_nome,
                "incentivo_produtivo_basico": item_pydantic.incentivo_produtivo_basico,
                "data_inclusao": item_pydantic.data_inclusao,
                "data_atualizacao": item_pydantic.data_atualizacao,
                "tem_resultado": item_pydantic.tem_resultado,
                "aplicabilidade_margem_preferencia_normal": item_pydantic.aplicabilidade_margem_preferencia_normal,
                "aplicabilidade_margem_preferencia_adicional": item_pydantic.aplicabilidade_margem_preferencia_adicional,
                "percentual_margem_preferencia_normal": item_pydantic.percentual_margem_preferencia_normal,
                "percentual_margem_preferencia_adicional": item_pydantic.percentual_margem_preferencia_adicional,
                "ncm_nbs_codigo": item_pydantic.ncm_nbs_codigo,
                "ncm_nbs_descricao": item_pydantic.ncm_nbs_descricao,
                "catalogo": item_pydantic.catalogo,
                "categoria_item_catalogo": item_pydantic.categoria_item_catalogo,
                "catalogo_codigo_item": item_pydantic.catalogo_codigo_item,
                "informacao_complementar": item_pydantic.informacao_complementar,
                "tipo_margem_preferencia": item_pydantic.tipo_margem_preferencia,
                "exigencia_conteudo_nacional": item_pydantic.exigencia_conteudo_nacional,
                "patrimonio": item_pydantic.patrimonio,
                "codigo_registro_imobiliario": item_pydantic.codigo_registro_imobiliario,
                "imagem": item_pydantic.imagem,
            }

            # Busca item existente
            item_existente = await self.get_by_contratacao_and_numero(
                numero_controle_pncp, item_pydantic.numero_item
            )

            if item_existente:
                # Atualiza dados existentes
                for key, value in dados_item.items():
                    setattr(item_existente, key, value)
                itens_salvos.append(item_existente)
            else:
                # Cria novo item
                item_novo = ItemContratacao(**dados_item)
                self.session.add(item_novo)
                itens_salvos.append(item_novo)

        return itens_salvos

    async def get_by_contratacao(
        self, numero_controle_pncp: str
    ) -> List[ItemContratacao]:
        """
        Busca todos os itens de uma contratação.

        Args:
            numero_controle_pncp: Número de controle da contratação

        Returns:
            Lista de ItemContratacao
        """
        stmt = (
            select(ItemContratacao)
            .where(ItemContratacao.numero_controle_pncp == numero_controle_pncp)
            .order_by(ItemContratacao.numero_item)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
