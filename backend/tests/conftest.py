"""Pytest configuration and fixtures."""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.config import settings
from src.database import Base, get_db
from src.main import app

# Import all ORM models to register them with Base.metadata
from src.models import (  # noqa: F401
    BookORM,
    BookVersionORM,
    ClubMeetingORM,
    ClubORM,
    MeetingORM,
    PageORM,
    PublisherORM,
    UserORM,
    UserSecurityORM,
)

# Create test database engine
test_engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=True,
)

# Create test session factory
TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Create an event loop for the test session.

    Yields:
        asyncio.AbstractEventLoop: The event loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session.

    Yields:
        AsyncSession: Database session for testing.
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with TestSessionLocal() as session:
        yield session

    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with database session override.

    Args:
        db_session: Test database session.

    Yields:
        AsyncClient: HTTP client for testing.
    """

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
