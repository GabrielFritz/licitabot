# PNCP Ingestion Service Dockerfile

FROM python:3.11-slim

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
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ingestor/ ./ingestor/

# Set Python path
ENV PYTHONPATH=/app

# Default command
CMD ["python", "ingestor/consumer.py"] 