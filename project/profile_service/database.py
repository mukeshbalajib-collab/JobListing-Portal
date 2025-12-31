"""
database.py

Async SQLAlchemy engine/session setup for PostgreSQL for the Profile service.
"""

import os
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


def _get_database_url() -> str:
	"""
	Get the database URL from the environment.
	By default, falls back to a local Postgres instance for development.
	"""
	url = os.getenv("PROFILE_DATABASE_URL") or os.getenv("DATABASE_URL")
	if not url:
		# Match the auth-service local default (password contains '@' encoded as %40)
		url = "postgresql+asyncpg://postgres:bavaguru12@localhost:5432/job_listing_db"
	return url


DATABASE_URL = _get_database_url()

# echo can be toggled for debugging SQL queries
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
	bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
	"""
	FastAPI dependency that provides an AsyncSession per request.
	"""
	async with AsyncSessionLocal() as session:
		yield session


