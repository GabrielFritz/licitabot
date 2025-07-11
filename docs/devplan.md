# Plano de Desenvolvimento

## 📋 Organização geral

- 🔵 Épico: macroobjetivo funcional
- 🟢 User Story: necessidade do usuário
- 🧩 Tarefa Técnica: implementação de backend, frontend ou infra
- 🔢 Ordem sugerida: (1) → (2) → ...

## 🔵 EPIC 1 — Ingestão dos Pregões

Garantir ingestão automatizada, estruturada e confiável dos dados do PNCP.

### 🟢 US 1.1

> Como operador do sistema, quero importar pregões eletrônicos do PNCP para poder recomendar itens a usuários.

#### Tarefas técnicas (US 1.1)

- [1.1.1](./devplan/EPIC1/US1.1/1.1.1.md) Criar worker ingestor com consumer.py para escutar fila RabbitMQ
- [1.1.2](./devplan/EPIC1/US1.1/1.1.2.md) Criar publisher no backend para acionar ingestão manualmente
- [1.1.3](./devplan/EPIC1/US1.1/1.1.3.md) Implementar fetch e parse da API do PNCP (somente pregões eletrônicos)
- [1.1.4](./devplan/EPIC1/US1.1/1.1.4.md) Criar estrutura de tabelas no Postgres: pregoes, itens_pregao
- [1.1.5](./devplan/EPIC1/US1.1/1.1.5.md) Salvar e normalizar os dados extraídos (UTF-8, unidades, datas etc.)
- [1.1.6](./devplan/EPIC1/US1.1/1.1.6.md) Agendar execução diária (ou periódica) da ingestão automática
- [1.1.7](./devplan/EPIC1/US1.1/1.1.7.md) Criar endpoint /sync/status e /sync/force (admin)

## 🔵 EPIC 2 — Sistema de Interesses

Permitir que o usuário cadastre o que ele busca para gerar recomendações personalizadas.

### 🟢 US 2.1

> Como usuário, quero cadastrar um interesse para receber pregões que combinem com ele.

#### Tarefas técnicas (US 2.1)

- [2.1.1](./devplan/EPIC2/US2.1/2.1.1.md) Criar tabela interesses (usuário_id, nome, texto, filtros, data_criacao)
- [2.1.2](./devplan/EPIC2/US2.1/2.1.2.md) Implementar CRUD de interesses via API REST
- [2.1.3](./devplan/EPIC2/US2.1/2.1.3.md) Implementar frontend /interests com form de criação + listagem
- [2.1.4](./devplan/EPIC2/US2.1/2.1.4.md) Criar UI de filtros básicos: palavras-chave, órgão, estado, valor mínimo/máximo
- [2.1.5](./devplan/EPIC2/US2.1/2.1.5.md) Validar e persistir interesses com Pydantic no backend

## 🔵 EPIC 3 — Matching Inteligente

Associar automaticamente os itens de pregão mais relevantes a cada interesse do usuário.

### 🟢 US 3.1

> Como usuário, quero ver os pregões (e itens) mais relevantes para os meus interesses.

#### Tarefas técnicas (US 3.1)

- [3.1.1](./devplan/EPIC3/US3.1/3.1.1.md) Gerar embeddings dos interesses (sentence-transformers, pgvector)
- [3.1.2](./devplan/EPIC3/US3.1/3.1.2.md) Gerar embeddings dos itens de pregão (descricao)
- [3.1.3](./devplan/EPIC3/US3.1/3.1.3.md) Implementar matching com RRF (cosine + trigram + FTS) por item
- [3.1.4](./devplan/EPIC3/US3.1/3.1.4.md) Salvar matches em matches (interesse_id, item_id, score, data)
- [3.1.5](./devplan/EPIC3/US3.1/3.1.5.md) Expor API /matches com filtro por interesse e ordenação por score

## 🔵 EPIC 4 — Dashboard e Consumo

Oferecer ao usuário um painel claro com os resultados do sistema.

### 🟢 US 4.1

> Como usuário, quero visualizar de forma fácil os pregões e itens recomendados para mim.

#### Tarefas técnicas (US 4.1)

- [4.1.1](./devplan/EPIC4/US4.1/4.1.1.md) Implementar frontend /dashboard com listagem dos matches
- [4.1.2](./devplan/EPIC4/US4.1/4.1.2.md) Exibir grupo por edital → expandir para ver os itens
- [4.1.3](./devplan/EPIC4/US4.1/4.1.3.md) Criar UI com destaque visual (score, tempo restante, órgão)
- [4.1.4](./devplan/EPIC4/US4.1/4.1.4.md) Link para página /matches/[id] com detalhes do item + edital

## 🔵 EPIC 5 — Alerta por E-mail

Gerar notificações por e-mail para manter o usuário informado sem depender do login.

### 🟢 US 5.1

> Como usuário, quero receber alertas por e-mail com itens relevantes que foram encontrados para mim.

#### Tarefas técnicas (US 5.1)

- [5.1.1](./devplan/EPIC5/US5.1/5.1.1.md) Criar serviço de envio de e-mails (alert_worker.py)
- [5.1.2](./devplan/EPIC5/US5.1/5.1.2.md) Criar template básico de digest diário (até X itens relevantes)
- [5.1.3](./devplan/EPIC5/US5.1/5.1.3.md) Agendar envio de digest diário usando job agendado
- [5.1.4](./devplan/EPIC5/US5.1/5.1.4.md) Configurar Mailgun/Resend/Postmark (via API)
- [5.1.5](./devplan/EPIC5/US5.1/5.1.5.md) Criar endpoint de opt-in/opt-out de e-mail (/notifications)

## 🔵 EPIC 6 — Autenticação e Conta

Controlar acesso e início de uso do sistema.

### 🟢 US 6.1

> Como usuário, quero criar conta e logar para poder cadastrar interesses e receber alertas.

#### Tarefas técnicas (US 6.1)

- [6.1.1](./devplan/EPIC6/US6.1/6.1.1.md) Configurar NextAuth com JWT
- [6.1.2](./devplan/EPIC6/US6.1/6.1.2.md) Criar páginas de login, cadastro e logout
- [6.1.3](./devplan/EPIC6/US6.1/6.1.3.md) Proteger rotas autenticadas (/dashboard, /interests)
- [6.1.4](./devplan/EPIC6/US6.1/6.1.4.md) Associar user_id em todas as queries de backend

## 🔵 EPIC 7 — Plano Gratuito e Trial

Controle de acesso às funcionalidades por plano.

### 🟢 US 7.1

> Como usuário gratuito, quero ter acesso limitado para entender o valor da plataforma.

#### Tarefas técnicas (US 7.1)

- [7.1.1](./devplan/EPIC7/US7.1/7.1.1.md) Implementar controle de plano por usuário (plano: free, pro)
- [7.1.2](./devplan/EPIC7/US7.1/7.1.2.md) Limitar criação de interesses (máx. 2 para plano gratuito)
- [7.1.3](./devplan/EPIC7/US7.1/7.1.3.md) Criar lógica de trial de 7 dias com Stripe + cancelamento
- [7.1.4](./devplan/EPIC7/US7.1/7.1.4.md) Adicionar CTAs para upgrade quando limite for atingido