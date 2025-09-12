FROM python:3.11-slim as base

WORKDIR /app

RUN pip install --upgrade pip

COPY pyproject.toml .

RUN pip install -e .

FROM base as raw-contratacao-ingestion-consumer

CMD ["raw-contratacao-ingestion-consumer"]

FROM base as licitabot-scheduler

CMD ["licitabot-scheduler"]
