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
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY licitabot/ ./licitabot/

# Set Python path
ENV PYTHONPATH=/app

FROM base as pncp_ingestion_consumer

CMD ["faststream", "run", "licitabot.presentation.pncp_ingestion_consumer.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

FROM base as pncp_ingestion_api

CMD ["uvicorn", "licitabot.presentation.pncp_ingestion_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

FROM base as embeddings_api

CMD ["uvicorn", "licitabot.presentation.embeddings_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
