# Stack Técnica e Arquitetura

Com base nos requisitos, a arquitetura técnica proposta para o MVP utiliza uma stack moderna, focada em rapidez de desenvolvimento, baixo custo inicial e suporte nativo a recursos de IA e escalabilidade.

## Backend (API RESTful)

Implementado em FastAPI (Python), estruturado em serviços ou módulos responsáveis por diferentes domínios (ex.: serviço de licitações, serviço de usuários, serviço de notificações). O FastAPI oferece excelente desempenho assíncrono e facilidade para escrever endpoints e lógica de negócio. Por exemplo, um endpoint GET /pregoes?categoria=X retornará pregões filtrados, enquanto um POST /usuarios/{id}/alertas permite configurar um novo alerta. A lógica de **coleta de dados** (ingestão via API do PNCP) será tratada por um serviço separado — não acoplado ao backend — que expõe um **consumer** (`consumer.py`) escutando uma **fila RabbitMQ**. Quando acionado, esse worker realiza a ingestão dos dados mais recentes, processa, normaliza e grava no banco (PostgreSQL). Esse padrão permite desacoplar ingestão e API, garantindo escalabilidade e modularidade.

Endpoints administrativos da API poderão fornecer:

- Status de sincronização
- Última execução da ingestão
- Forçar atualização (via publish RabbitMQ)

Validações de dados e esquema serão tratados com Pydantic (integrado ao FastAPI).

### Relevantes à stack

- **FastAPI** (Python)
- **Pydantic**, **SQLAlchemy**
- **RabbitMQ** para fila de ingestão
- **Serviço dedicado** de ingestão com `consumer.py`
- **PostgreSQL** com extensões:
  - `pgvector` para embeddings semânticos
  - `TSVector` para busca full-text

## Frontend

Next.js (React) para construir uma SPA rica em interatividade, com SSR para melhor SEO nas páginas públicas. O Next.js será usado tanto para o site institucional (apresentando o produto, planos, blog educativo sobre licitações) quanto para o aplicativo web do usuário (dashboard). Componentes React permitirão atualizações em tempo real (ex.: usar WebSockets ou SSE via FastAPI para push de novos pregões e alertas no dashboard sem recarregar). Adotar Next.js traz também a flexibilidade de servir uma página de pregão com URL estável (ex: /pregao/2025/07/12345) que pode ser indexada pelos buscadores – ajudando no marketing orgânico. Para UI/UX, poderemos usar um kit de componentes moderno (por ex. Material UI ou Chakra) para ganhar agilidade e responsividade mobile.

### Relevantes à stack de Frontend

- Next.js 14
- TailwindCSS + ShadCN
- Auth: NextAuth + JWT

## Banco de Dados

PostgreSQL 15+ será o core database, escolhida pela robustez e familiaridade do mercado. Utilizaremos a extensão pgvector para armazenar e indexar vetores de embedding de texto, possibilitando buscas semânticas e ranking por similaridade. A estrutura inicial de tabelas inclui: licitacoes (com campos do PNCP como id, descrição, órgão, datas, situação), editais_texto (conteúdo textual extraído dos editais, talvez segmentado por seção, com seus vetores correspondentes para IA), usuarios (dados de login/governo), preferencias (palavras-chave, filtros salvos por usuário), alertas (configurações e histórico de notificações enviadas) etc. Consultas complexas poderão combinar busca por texto (LIKE ou TSVector) e por vetores (função <-> do pgvector para distância cosinus). O Postgres também garantirá ACID para atualizar status (ex.: marcar que o usuário X está interessado no pregão Y).

### Relevantes à stack de Banco de Dados

- PostgreSQL 15+
- Extensões: pgvector, pg_trgm
- Tabelas: licitacoes, interesses, matches, alertas, usuarios

## Ingestão de Dados PNCP

Um componente dedicado fará a interface com a API do PNCP. Pode ser implementado como um módulo Python reusado (chamado pelo FastAPI em background tasks, ou rodado separadamente via RabbitMQ queue). Esse módulo gerencia credenciais e tokens necessários (se houver; o PNCP exige credenciamento para publicação, mas para leitura os dados são públicos). Ele chamará endpoints de dados do PNCP (por exemplo, listas de editais publicados recentemente em JSON ou XML) e fará parse e persistência no Postgres. Qualquer documento PDF de edital será baixado e, se possível, passado por um OCR/extrator de texto (usando ferramentas Python como PDFMiner ou PyMuPDF) para armazenar o texto em editais_texto. Essa extração textual é fundamental para os recursos de IA. Vale destacar que, por ser uma integração central, um único desenvolvimento atende todos os órgãos integrados – diferente do antigo cenário com múltiplos crawlers por portal. Isso reduz complexidade no MVP.

## Camada de IA

Para habilitar resumos e recomendações inteligentes, integraremos modelos de IA. A arquitetura aqui pode variar: inicialmente, usar serviços externos via API (SaaS de NLP) para tarefas on-demand como resumo de edital ou resposta a perguntas. O FastAPI pode expor internamente uma função resumir_texto(texto) que envia o texto a um endpoint de IA (ex.: OpenAI, Azure Cognitive, etc.) e retorna o resumo. Manteremos também um servidor de embeddings: utilizando bibliotecas como HuggingFace Transformers ou SentenceTransformers no backend para gerar vetores a partir de textos (por exemplo, usar um modelo multilíngue tipo all-MiniLM-L6-v2 ou similar compatível com português). Alternativamente, podemos armazenar embeddings precomputados gerados offline. A escolha por pgvector no Postgres se justifica aqui: consultas de similaridade podem ser feitas diretamente no banco (ex.: “recuperar os 5 editais mais semanticamente parecidos com a descrição X”). Essa arquitetura de IA embutida facilitará implementar recursos como “licitações semelhantes” e ranking personalizado.

## Serviços de Notificação

Para enviar emails e notificações, integraremos serviços como SMTP (para email) e possivelmente Firebase Cloud Messaging ou similar para push notifications móveis (caso tenhamos app mobile ou PWA). O MVP pode começar com notificações via email, escalando para push conforme demanda. Em termos de arquitetura, o FastAPI pode enviar emails de forma assíncrona (usando ThreadPool ou Celery worker) para não bloquear requisições. Templates de email serão armazenados e conterão os links para o sistema. Garantir entrega (via um provedor confiável como SendGrid ou AWS SES) também é parte técnica importante para a experiência do usuário.

## DevOps e Implantação

Para acelerar o lançamento, podemos usar um ambiente PaaS ou container orchestration simples. Recomenda-se Docker para padronizar ambientes de desenvolvimento e produção. Em MVP, uma opção ágil é usar serviços como Heroku ou Fly.io (que suportam FastAPI + Postgres facilmente) ou então configurar uma VPS na AWS/Google Cloud e rodar os containers (ex.: com Docker Compose ou em uma pequena instância Kubernetes se houver conhecimento). A aplicação será dividida em contêineres: um para o backend, um para o frontend (que pode ser servido estático via CDN após build), e o banco em serviço gerenciado. Configuração de CI/CD (por exemplo, GitHub Actions) para automatizar deploys em staging e produção é desejável para iterar rapidamente. Além disso, implementar monitoramento (logs centralizados, APM básico como Sentry para erros do frontend/backend) e backup diário do banco são partes da arquitetura desde o MVP, visando confiabilidade.

### Relevantes à stack de DevOps e Implantação

- Docker
- DigitalOcean App Platform / Fly.io
- CI/CD com GitHub Actions
- Observabilidade: Sentry, Grafana Cloud, Logtail
