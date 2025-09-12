FROM python:3.11-slim as base

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip

COPY . .

RUN pip install -e .

FROM base as raw-contratacao-ingestion-consumer

CMD ["raw-contratacao-ingestion-consumer"]

FROM base as licitabot-scheduler

CMD ["licitabot-scheduler"]
