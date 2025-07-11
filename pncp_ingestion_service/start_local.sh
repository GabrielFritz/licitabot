#!/bin/bash

# PNCP Ingestion Service - Local Development Startup Script

set -e

echo "🚀 Starting PNCP Ingestion Service (Local Development)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed. Please install it and try again."
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

print_status "Starting RabbitMQ..."
docker-compose up -d rabbitmq

print_status "Waiting for RabbitMQ to be ready..."
sleep 10

print_status "Testing RabbitMQ connection..."
python tests/test_rabbitmq.py

if [ $? -eq 0 ]; then
    print_success "RabbitMQ is ready!"
    
    echo ""
    print_status "Starting PNCP Ingestion Service..."
    print_status "Press Ctrl+C to stop all services"
    echo ""
    
    # Start the ingestion service
    docker-compose up pncp-ingestor
    
else
    print_error "RabbitMQ test failed. Please check the logs:"
    docker-compose logs rabbitmq
    exit 1
fi 