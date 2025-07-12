# Configuração de Variáveis de Ambiente

## 📋 Setup Inicial

1. **Copie o arquivo de exemplo:**
   ```bash
   cp env.local.example .env.local
   ```

2. **Edite o .env.local conforme necessário:**
   ```bash
   nano .env.local
   ```

## 🔧 Variáveis de Ambiente

### **RabbitMQ Configuration**
```bash
QUEUE_NAME=ingest.pncp                    # Nome da fila RabbitMQ
RABBITMQ_URL=amqp://admin:admin123@rabbitmq:5672/  # URL do RabbitMQ
```

### **PostgreSQL Configuration**
```bash
POSTGRES_HOST=postgres                    # Host do PostgreSQL
POSTGRES_PORT=5432                        # Porta do PostgreSQL
POSTGRES_DB=pncp_ingestion               # Nome do banco
POSTGRES_USER=pncp_user                  # Usuário do banco
POSTGRES_PASSWORD=pncp_pass              # Senha do banco
```

### **Database Connection Settings**
```bash
DB_POOL_SIZE=10                          # Tamanho do pool de conexões
DB_MAX_OVERFLOW=20                       # Overflow máximo do pool
DB_POOL_TIMEOUT=30                       # Timeout do pool (segundos)
DB_POOL_RECYCLE=300                      # Reciclagem do pool (segundos)
```

### **Ingestion Configuration**
```bash
ROLLING_WINDOW_MINUTES=15                # Janela de ingestão (minutos)
HTTP_TIMEOUT=20.0                        # Timeout HTTP (segundos)
```

### **Logging Configuration**
```bash
LOG_LEVEL=INFO                           # Nível de log (DEBUG, INFO, WARNING, ERROR)
LOG_FORMAT=[%(asctime)s] %(levelname)s: %(message)s  # Formato do log
```

### **Development Configuration**
```bash
DEBUG=true                               # Modo debug (true/false)
TESTING=false                            # Modo teste (true/false)
```

### **Timezone**
```bash
TZ=America/Cuiaba                       # Fuso horário
```

## 🚀 Como Usar

### **Desenvolvimento Local:**
```bash
# 1. Configure o .env.local
cp env.local.example .env.local

# 2. Edite as variáveis conforme necessário
nano .env.local

# 3. Execute os testes
./run_tests.sh

# 4. Execute o serviço
./start_local.sh
```

### **Docker Compose:**
```bash
# O docker-compose.yaml já está configurado para usar .env.local
docker-compose up -d
```

## 🔍 Verificação

Para verificar se as variáveis estão sendo carregadas corretamente:

```bash
# Execute os testes
./run_tests.sh

# Verifique os logs
docker-compose logs pncp-ingestor
```

## 📝 Notas

- **Desenvolvimento:** Use `DEBUG=true` para logs detalhados
- **Testes:** Use `TESTING=true` para ambiente de teste
- **Produção:** Use `DEBUG=false` e `TESTING=false`
- **Banco:** As configurações do PostgreSQL são para containers Docker 