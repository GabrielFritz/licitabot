# PNCP Ingestion Service

Micro-serviço desacoplado para ingestão de dados do PNCP (Portal Nacional de Contratações Públicas).

## 🎯 Funcionalidades

- **Escuta** a fila `ingest.pncp` no RabbitMQ
- Processa mensagens JSON com modos **update** e **backfill**
- Faz requisições à API PNCP com paginação inteligente
- Filtra dados por janela temporal em memória
- Coleta itens de contratação para cada contrato

## 🚀 Execução

### Opção 1: Docker Compose (Recomendado)

```bash
# Iniciar todos os serviços
docker-compose up

# Ou apenas RabbitMQ para desenvolvimento local
docker-compose up -d rabbitmq

# Testar conexão e enviar mensagens de teste
python tests/test_local.py

# Executar o serviço de ingestão
python ingestor/consumer.py
```

### Opção 2: Script Automatizado

```bash
# Script que configura tudo automaticamente
./start_local.sh
```

### Opção 3: Execução Manual

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar RabbitMQ
docker-compose up -d rabbitmq

# Testar conexão
python tests/test_rabbitmq.py

# Executar serviço
python ingestor/consumer.py
```

## 🧪 Testes

### Executar Todos os Testes

```bash
# Pré-requisito: RabbitMQ deve estar rodando
docker-compose up -d rabbitmq

# Executar todos os testes (incluindo async)
python tests/run_all_tests.py
```

### Testes Individuais

```bash
# Testar funções utils (não requer RabbitMQ)
python tests/test_utils.py

# Testar conexão RabbitMQ (requer RabbitMQ rodando)
python tests/test_rabbitmq.py

# Testar desenvolvimento local (requer RabbitMQ rodando)
python tests/test_local.py
```

### Testes com Docker Compose

```bash
# Executar testes em container (requer RabbitMQ)
docker-compose --profile test up pncp-tests

# Ou executar tudo junto
docker-compose --profile test up
```

## ⚙️ Configuração

### Variáveis de Ambiente (.env.local)

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `QUEUE_NAME` | `ingest.pncp` | Nome da fila RabbitMQ |
| `RABBITMQ_URL` | `amqp://admin:admin123@rabbitmq:5672/` | URL do RabbitMQ |
| `ROLLING_WINDOW_MINUTES` | `15` | Janela para modo update (minutos) |
| `HTTP_TIMEOUT` | `20.0` | Timeout das requisições HTTP (segundos) |
| `DEBUG` | `true` | Modo debug |
| `LOG_LEVEL` | `DEBUG` | Nível de log |

### Serviços Docker Compose

- **RabbitMQ**: `localhost:5672` (AMQP), `localhost:15672` (Management UI)
- **PNCP Ingestion**: Container com o serviço de ingestão
- **PNCP Tests**: Container para executar testes (profile: test)
- **Redis**: `localhost:6379` (opcional, para cache futuro)

### Credenciais RabbitMQ

- **URL**: `amqp://admin:admin123@rabbitmq:5672/`
- **Management UI**: <http://localhost:15672>
- **Usuário**: `admin`
- **Senha**: `admin123`

## 📨 Mensagens Aceitas

### Modo Update (padrão)

```json
{}
```

ou

```json
{"mode": "update"}
```

### Modo Backfill

```json
{
  "mode": "backfill",
  "data_ini": "2025-01-10T12:00:00",
  "data_fim": "2025-01-10T18:00:00"
}
```

## 📊 Estrutura do Projeto

```text
pncp_ingestion_service/
├── ingestor/
│   ├── consumer.py          # Worker RabbitMQ
│   ├── services/
│   │   └── ingestion.py     # Lógica de ingestão
│   ├── models/
│   │   └── pncp.py          # Modelos Pydantic
│   ├── utils.py             # Funções auxiliares
│   └── config.py            # Configuração centralizada
├── tests/
│   ├── __init__.py          # Package init
│   ├── test_utils.py        # Testes das funções utils
│   ├── test_rabbitmq.py     # Teste de conexão RabbitMQ
│   ├── test_local.py        # Teste para desenvolvimento local
│   └── run_all_tests.py     # Executor de todos os testes
├── requirements.txt          # Dependências Python
├── docker-compose.yaml       # Orquestração local
├── Dockerfile               # Containerização
├── .env.local               # Variáveis de ambiente
├── start_local.sh           # Script de inicialização
└── README.md               # Esta documentação
```

## 🔧 Desenvolvimento

### Logs e Monitoramento

```bash
# Ver logs do RabbitMQ
docker-compose logs rabbitmq

# Ver logs do serviço de ingestão
docker-compose logs pncp-ingestor

# Acompanhar logs em tempo real
docker-compose logs -f pncp-ingestor

# Ver logs dos testes
docker-compose logs pncp-tests
```

### RabbitMQ Management UI

Acesse <http://localhost:15672> para:

- Visualizar filas e mensagens
- Monitorar conexões
- Enviar mensagens de teste
- Ver estatísticas de performance

## 📝 Logs

O serviço imprime logs no formato:

```text
[ingestor] mode=update  window=2025-01-10T14:45:00 → 2025-01-10T15:00:00  (Δ=900s)
[✓] 07854402000100-1-000054/2025 2025-01-10T14:47:32 — 5 itens
```

## 🔄 Próximos Passos

- [ ] Persistência no PostgreSQL
- [ ] Publicação em fila `ingest.persist`
- [ ] Métricas e monitoramento
- [ ] Tratamento de erros robusto
- [ ] Testes automatizados
