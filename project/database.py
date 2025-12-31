"""
database.py

Async SQLAlchemy engine/session setup for PostgreSQL.
"""

import os
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

def _get_database_url() -> str:
    """
    Get the database URL from the environment, with a sensible local default.
    The URL looks like: postgresql+asyncpg://user:password@host:5432/dbname
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        # UPDATED: Using your confirmed password and database name
        url = "postgresql+asyncpg://postgres:bavaguru12@localhost:5432/job_listing_db"
    return url

DATABASE_URL = _get_database_url()

# Create the async engine for PostgreSQL 18
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Setup the session maker
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """
    FastAPI dependency that provides an AsyncSession per request.
    """
    async with AsyncSessionLocal() as session:
        yield session