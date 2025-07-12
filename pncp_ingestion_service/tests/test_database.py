"""
Test database connectivity and basic operations.
Runs only inside Docker containers.
"""

import asyncio
import os
import sys
from unittest import TestCase

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import text
from ingestor.database.connection import get_sync_engine, get_async_engine, db_config
from ingestor.database.models import Base
from ingestor.config import settings


class TestDatabaseConnection(TestCase):
    """Test database connectivity and basic operations."""

    def setUp(self):
        """Set up test environment."""
        # Environment variables are set by docker-compose
        pass

    def test_sync_connection(self):
        """Test synchronous database connection."""
        try:
            engine = get_sync_engine()
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                self.assertEqual(result.scalar(), 1)
            print("✅ Sync database connection successful")
        except Exception as e:
            self.fail(f"Sync database connection failed: {e}")

    def test_async_connection(self):
        """Test asynchronous database connection."""

        async def test_async():
            try:
                engine = get_async_engine()
                async with engine.connect() as connection:
                    result = await connection.execute(text("SELECT 1"))
                    value = result.scalar()
                    self.assertEqual(value, 1)
                print("✅ Async database connection successful")
            except Exception as e:
                self.fail(f"Async database connection failed: {e}")

        asyncio.run(test_async())

    def test_create_tables(self):
        """Test creating database tables."""
        try:
            engine = get_sync_engine()
            Base.metadata.create_all(engine)
            print("✅ Database tables created successfully")
        except Exception as e:
            self.fail(f"Failed to create database tables: {e}")

    def test_database_url_generation(self):
        """Test database URL generation."""
        url = db_config.database_url
        self.assertIn("postgresql://", url)
        self.assertIn(settings.POSTGRES_USER, url)
        self.assertIn(settings.POSTGRES_PASSWORD, url)
        self.assertIn(f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}", url)
        self.assertIn(settings.POSTGRES_DB, url)
        print("✅ Database URL generation successful")

    def test_async_database_url_generation(self):
        """Test async database URL generation."""
        url = db_config.async_database_url
        self.assertIn("postgresql+asyncpg://", url)
        self.assertIn(settings.POSTGRES_USER, url)
        self.assertIn(settings.POSTGRES_PASSWORD, url)
        self.assertIn(f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}", url)
        self.assertIn(settings.POSTGRES_DB, url)
        print("✅ Async database URL generation successful")

    def test_settings_loaded(self):
        """Test that settings are properly loaded."""
        self.assertEqual(settings.POSTGRES_HOST, "postgres")
        self.assertEqual(settings.POSTGRES_DB, "pncp_ingestion")
        self.assertEqual(settings.POSTGRES_USER, "pncp_user")
        self.assertTrue(settings.DEBUG)
        print("✅ Settings loaded correctly")

    def tearDown(self):
        """Clean up after tests."""
        db_config.close()


def run_database_tests():
    """Run all database tests."""
    import unittest

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseConnection)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_database_tests()
    sys.exit(0 if success else 1)
