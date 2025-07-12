#!/usr/bin/env python3
"""
Database initialization script for PNCP Ingestion Service.

This script:
1. Creates the database if it doesn't exist
2. Runs Alembic migrations
3. Creates initial indexes
4. Validates the setup
"""
import os
import sys
import subprocess
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ingestor.database.connection import get_sync_engine, db_config
from ingestor.database.models import Base


def wait_for_postgres(max_retries=30, delay=2):
    """Wait for PostgreSQL to be ready."""
    print("🔄 Waiting for PostgreSQL to be ready...")

    for attempt in range(max_retries):
        try:
            engine = get_sync_engine()
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            print("✅ PostgreSQL is ready!")
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(
                    f"⏳ PostgreSQL not ready yet (attempt {attempt + 1}/{max_retries}): {e}"
                )
                time.sleep(delay)
            else:
                print(
                    f"❌ Failed to connect to PostgreSQL after {max_retries} attempts"
                )
                return False

    return False


def create_database():
    """Create database tables using SQLAlchemy."""
    try:
        print("🔄 Creating database tables...")
        engine = get_sync_engine()
        Base.metadata.create_all(engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        return False


def run_migrations():
    """Run Alembic migrations."""
    try:
        print("🔄 Running Alembic migrations...")

        # Change to project root directory
        os.chdir(project_root)

        # Run alembic upgrade
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=project_root,
        )

        if result.returncode == 0:
            print("✅ Alembic migrations completed successfully")
            return True
        else:
            print(f"❌ Alembic migrations failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Failed to run migrations: {e}")
        return False


def validate_database():
    """Validate database setup by checking if tables exist."""
    try:
        print("🔄 Validating database setup...")
        engine = get_sync_engine()

        # Check if main tables exist
        expected_tables = [
            "orgaos_entidades",
            "unidades_orgaos",
            "amparos_legais",
            "fontes_orcamentarias",
            "contratacoes",
            "itens_contratacao",
            "contratacoes_fontes_orcamentarias",
        ]

        with engine.connect() as connection:
            for table in expected_tables:
                result = connection.execute(f"SELECT 1 FROM {table} LIMIT 1")
                print(f"✅ Table '{table}' exists")

        print("✅ Database validation completed successfully")
        return True

    except Exception as e:
        print(f"❌ Database validation failed: {e}")
        return False


def main():
    """Main initialization function."""
    print("🚀 Initializing PNCP Ingestion Database...")
    print("=" * 50)

    # Step 1: Wait for PostgreSQL
    if not wait_for_postgres():
        print("❌ Failed to connect to PostgreSQL")
        sys.exit(1)

    # Step 2: Create database tables
    if not create_database():
        print("❌ Failed to create database tables")
        sys.exit(1)

    # Step 3: Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations")
        sys.exit(1)

    # Step 4: Validate setup
    if not validate_database():
        print("❌ Database validation failed")
        sys.exit(1)

    print("=" * 50)
    print("🎉 Database initialization completed successfully!")
    print("📊 Database is ready for PNCP data ingestion")

    # Clean up
    db_config.close()


if __name__ == "__main__":
    main()
