# PNCP Ingestion Service Dockerfile

FROM python:3.11-slim as base

# Set timezone to America/Cuiabá (Brazil)
ENV TZ=America/Cuiaba
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Copy project configuration
COPY pyproject.toml .

# Install the project in editable mode
RUN pip install -e .

# Set Python path
ENV PYTHONPATH=/app

FROM base as pncp_ingestion_consumer

CMD ["uvicorn", "licitabot.presentation.pncp_ingestion_consumer.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--reload"]

FROM base as pncp_ingestion_api

CMD ["uvicorn", "licitabot.presentation.pncp_ingestion_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--reload"]

FROM base as embeddings_api

CMD ["uvicorn", "licitabot.presentation.embeddings_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--reload"]

FROM base as search_api

CMD ["uvicorn", "licitabot.presentation.search_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--reload"]

FROM base as test

CMD ["python", "/app/licitabot/test.py"]