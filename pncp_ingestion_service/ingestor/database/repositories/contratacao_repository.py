"""
Repositório para operações com contratações.
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ingestor.database.models import (
    Contratacao,
    AmparoLegal,
    FonteOrcamentaria,
    ContratacaoFonteOrcamentaria,
)
from ingestor.models.pncp import Contratacao as ContratacaoPydantic


class ContratacaoRepository:
    """Repositório para operações com contratações."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_numero_controle(
        self, numero_controle_pncp: str
    ) -> Optional[Contratacao]:
        """
        Busca contratação por número de controle PNCP.

        Args:
            numero_controle_pncp: Número de controle da contratação

        Returns:
            Contratacao ou None se não encontrado
        """
        if not numero_controle_pncp:
            return None

        stmt = select(Contratacao).where(
            Contratacao.numero_controle_pncp == numero_controle_pncp
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert_amparo_legal(self, amparo_pydantic) -> AmparoLegal:
        """
        Upsert amparo legal.

        Args:
            amparo_pydantic: Dados do amparo legal vindos da API

        Returns:
            AmparoLegal salvo/atualizado
        """
        stmt = select(AmparoLegal).where(AmparoLegal.codigo == amparo_pydantic.codigo)
        result = await self.session.execute(stmt)
        amparo_existente = result.scalar_one_or_none()

        if amparo_existente:
            # Atualiza dados existentes
            amparo_existente.nome = amparo_pydantic.nome
            amparo_existente.descricao = amparo_pydantic.descricao
            return amparo_existente
        else:
            # Cria novo amparo legal
            amparo_novo = AmparoLegal(
                codigo=amparo_pydantic.codigo,
                nome=amparo_pydantic.nome,
                descricao=amparo_pydantic.descricao,
            )
            self.session.add(amparo_novo)
            return amparo_novo

    async def upsert_fonte_orcamentaria(self, fonte_pydantic) -> FonteOrcamentaria:
        """
        Upsert fonte orçamentária.

        Args:
            fonte_pydantic: Dados da fonte orçamentária vindos da API

        Returns:
            FonteOrcamentaria salvo/atualizado
        """
        stmt = select(FonteOrcamentaria).where(
            FonteOrcamentaria.codigo == fonte_pydantic.codigo
        )
        result = await self.session.execute(stmt)
        fonte_existente = result.scalar_one_or_none()

        if fonte_existente:
            # Atualiza dados existentes
            fonte_existente.nome = fonte_pydantic.nome
            fonte_existente.descricao = fonte_pydantic.descricao
            fonte_existente.data_inclusao = fonte_pydantic.data_inclusao
            return fonte_existente
        else:
            # Cria nova fonte orçamentária
            fonte_nova = FonteOrcamentaria(
                codigo=fonte_pydantic.codigo,
                nome=fonte_pydantic.nome,
                descricao=fonte_pydantic.descricao,
                data_inclusao=fonte_pydantic.data_inclusao,
            )
            self.session.add(fonte_nova)
            return fonte_nova

    async def upsert(
        self,
        contratacao_pydantic: ContratacaoPydantic,
        orgao_id: Optional[int] = None,
        unidade_id: Optional[int] = None,
        amparo_id: Optional[int] = None,
        unidade_sub_rogada_id: Optional[int] = None,
        orgao_sub_rogado_id: Optional[int] = None,
    ) -> Contratacao:
        """
        Upsert contratação baseado no numero_controle_pncp.

        Args:
            contratacao_pydantic: Dados da contratação vindos da API
            orgao_id: ID do órgão (opcional)
            unidade_id: ID da unidade (opcional)
            amparo_id: ID do amparo legal (opcional)
            unidade_sub_rogada_id: ID da unidade sub-rogada (opcional)
            orgao_sub_rogado_id: ID do órgão sub-rogado (opcional)

        Returns:
            Contratacao salvo/atualizado
        """
        # Busca contratação existente
        contratacao_existente = await self.get_by_numero_controle(
            contratacao_pydantic.numero_controle_pncp
        )

        # Dados da contratação
        dados_contratacao = {
            "numero_controle_pncp": contratacao_pydantic.numero_controle_pncp,
            "srp": contratacao_pydantic.srp,
            "data_inclusao": contratacao_pydantic.data_inclusao,
            "data_publicacao_pncp": contratacao_pydantic.data_publicacao_pncp,
            "data_atualizacao": contratacao_pydantic.data_atualizacao,
            "data_atualizacao_global": contratacao_pydantic.data_atualizacao_global,
            "data_abertura_proposta": contratacao_pydantic.data_abertura_proposta,
            "data_encerramento_proposta": contratacao_pydantic.data_encerramento_proposta,
            "ano_compra": contratacao_pydantic.ano_compra,
            "sequencial_compra": contratacao_pydantic.sequencial_compra,
            "numero_compra": contratacao_pydantic.numero_compra,
            "processo": contratacao_pydantic.processo,
            "modalidade_id": contratacao_pydantic.modalidade_id,
            "modalidade_nome": contratacao_pydantic.modalidade_nome,
            "modo_disputa_id": contratacao_pydantic.modo_disputa_id,
            "modo_disputa_nome": contratacao_pydantic.modo_disputa_nome,
            "objeto_compra": contratacao_pydantic.objeto_compra,
            "valor_total_estimado": contratacao_pydantic.valor_total_estimado,
            "valor_total_homologado": contratacao_pydantic.valor_total_homologado,
            "informacao_complementar": contratacao_pydantic.informacao_complementar,
            "justificativa_presencial": contratacao_pydantic.justificativa_presencial,
            "link_sistema_origem": contratacao_pydantic.link_sistema_origem,
            "link_processo_eletronico": contratacao_pydantic.link_processo_eletronico,
            "situacao_compra_id": (
                str(contratacao_pydantic.situacao_compra_id)
                if contratacao_pydantic.situacao_compra_id
                else None
            ),
            "situacao_compra_nome": contratacao_pydantic.situacao_compra_nome,
            "tipo_instrumento_convocatorio_codigo": contratacao_pydantic.tipo_instrumento_convocatorio_codigo,
            "tipo_instrumento_convocatorio_nome": contratacao_pydantic.tipo_instrumento_convocatorio_nome,
            "usuario_nome": contratacao_pydantic.usuario_nome,
        }

        # Adiciona foreign keys apenas se os IDs não forem None
        if orgao_id is not None:
            dados_contratacao["orgao_entidade_id"] = orgao_id
        if unidade_id is not None:
            dados_contratacao["unidade_orgao_id"] = unidade_id
        if amparo_id is not None:
            dados_contratacao["amparo_legal_id"] = amparo_id
        if unidade_sub_rogada_id is not None:
            dados_contratacao["unidade_sub_rogada_id"] = unidade_sub_rogada_id
        if orgao_sub_rogado_id is not None:
            dados_contratacao["orgao_sub_rogado_id"] = orgao_sub_rogado_id

        if contratacao_existente:
            # Atualiza dados existentes
            for key, value in dados_contratacao.items():
                setattr(contratacao_existente, key, value)
            return contratacao_existente
        else:
            # Cria nova contratação
            contratacao_nova = Contratacao(**dados_contratacao)
            self.session.add(contratacao_nova)
            return contratacao_nova

    async def get_or_create(
        self,
        contratacao_pydantic: ContratacaoPydantic,
        orgao_id: int,
        unidade_id: int,
        amparo_id: int,
        unidade_sub_rogada_id: Optional[int] = None,
        orgao_sub_rogado_id: Optional[int] = None,
    ) -> Contratacao:
        """
        Busca contratação ou cria se não existir.

        Args:
            contratacao_pydantic: Dados da contratação vindos da API
            orgao_id: ID do órgão
            unidade_id: ID da unidade
            amparo_id: ID do amparo legal
            unidade_sub_rogada_id: ID da unidade sub-rogada (opcional)
            orgao_sub_rogado_id: ID do órgão sub-rogado (opcional)

        Returns:
            Contratacao existente ou criado
        """
        return await self.upsert(
            contratacao_pydantic,
            orgao_id,
            unidade_id,
            amparo_id,
            unidade_sub_rogada_id,
            orgao_sub_rogado_id,
        )
