"""
Database connection configuration for PostgreSQL.
"""

from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import StaticPool

from ..config import settings


class DatabaseConfig:
    """Database configuration and connection management."""

    def __init__(self):
        self._sync_engine: Optional[Engine] = None
        self._async_engine: Optional[AsyncEngine] = None
        self._sync_session_factory: Optional[sessionmaker] = None
        self._async_session_factory: Optional[sessionmaker] = None

    @property
    def database_url(self) -> str:
        """Get database URL from settings."""
        return settings.database_url

    @property
    def async_database_url(self) -> str:
        """Get async database URL from settings."""
        return settings.async_database_url

    def get_sync_engine(self) -> Engine:
        """Get synchronous SQLAlchemy engine."""
        if self._sync_engine is None:
            self._sync_engine = create_engine(
                self.database_url,
                pool_pre_ping=True,
                pool_recycle=settings.DB_POOL_RECYCLE,
                echo=settings.DEBUG,
                poolclass=StaticPool if settings.TESTING else None,
            )
        return self._sync_engine

    def get_async_engine(self) -> AsyncEngine:
        """Get asynchronous SQLAlchemy engine."""
        if self._async_engine is None:
            self._async_engine = create_async_engine(
                self.async_database_url,
                pool_pre_ping=True,
                pool_recycle=settings.DB_POOL_RECYCLE,
                echo=settings.DEBUG,
                poolclass=StaticPool if settings.TESTING else None,
            )
        return self._async_engine

    def get_sync_session_factory(self) -> sessionmaker:
        """Get synchronous session factory."""
        if self._sync_session_factory is None:
            engine = self.get_sync_engine()
            self._sync_session_factory = sessionmaker(
                bind=engine, autocommit=False, autoflush=False
            )
        return self._sync_session_factory

    def get_async_session_factory(self) -> sessionmaker:
        """Get asynchronous session factory."""
        if self._async_session_factory is None:
            engine = self.get_async_engine()
            self._async_session_factory = sessionmaker(
                bind=engine, class_=AsyncSession, autocommit=False, autoflush=False
            )
        return self._async_session_factory

    def get_sync_session(self) -> Session:
        """Get synchronous database session."""
        session_factory = self.get_sync_session_factory()
        return session_factory()

    def get_async_session(self) -> AsyncSession:
        """Get asynchronous database session."""
        session_factory = self.get_async_session_factory()
        return session_factory()

    def close(self):
        """Close all database connections."""
        if self._sync_engine:
            self._sync_engine.dispose()
            self._sync_engine = None

        if self._async_engine:
            self._async_engine.dispose()
            self._async_engine = None

        self._sync_session_factory = None
        self._async_session_factory = None


# Global database configuration instance
db_config = DatabaseConfig()


def get_sync_session() -> Session:
    """Get synchronous database session."""
    return db_config.get_sync_session()


def get_async_session() -> AsyncSession:
    """Get asynchronous database session."""
    return db_config.get_async_session()


def get_sync_engine() -> Engine:
    """Get synchronous database engine."""
    return db_config.get_sync_engine()


def get_async_engine() -> AsyncEngine:
    """Get asynchronous database engine."""
    return db_config.get_async_engine()
