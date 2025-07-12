#!/bin/bash

# PNCP Ingestion Service - Test Runner Script

set -e

echo "🧪 Running PNCP Ingestion Service Tests"

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

print_status "Starting required services (PostgreSQL and RabbitMQ)..."
docker-compose up -d postgres rabbitmq

print_status "Waiting for services to be ready..."
sleep 20

print_status "Running all tests in container..."
docker-compose run --rm pncp-tests

if [ $? -eq 0 ]; then
    print_success "All tests passed!"
else
    print_error "Some tests failed!"
    exit 1
fi 