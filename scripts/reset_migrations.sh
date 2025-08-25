#!/bin/bash

set -e

echo "🗑️  Deleting everything inside migrations/"
rm -rf migrations/*

echo "🔨 Building init-db service..."
docker compose build init-db

echo "🚀 Running init-db service..."
docker compose run --rm init-db

echo "✅ Migration reset completed successfully!"
