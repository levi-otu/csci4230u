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
    ReadingListItemORM,
    ReadingListORM,
    UserBookORM,
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


# Library-specific fixtures

@pytest.fixture
async def auth_user(client: AsyncClient) -> dict:
    """
    Create and authenticate a test user.

    Args:
        client: Test HTTP client.

    Returns:
        dict: User data with access token.
    """
    # Register user
    register_response = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )

    assert register_response.status_code == 201
    token_data = register_response.json()

    return {
        "username": "testuser",
        "email": "test@example.com",
        "access_token": token_data["access_token"],
        "token_type": token_data["token_type"]
    }


@pytest.fixture
async def auth_headers(auth_user: dict) -> dict:
    """
    Get authorization headers for authenticated requests.

    Args:
        auth_user: Authenticated user data.

    Returns:
        dict: Authorization headers.
    """
    return {
        "Authorization": f"{auth_user['token_type']} {auth_user['access_token']}"
    }


@pytest.fixture
async def sample_book(client: AsyncClient, auth_headers: dict) -> dict:
    """
    Create a sample book in the catalog.

    Args:
        client: Test HTTP client.
        auth_headers: Authorization headers.

    Returns:
        dict: Created book data.
    """
    response = await client.post(
        "/api/library/books",
        headers=auth_headers,
        json={
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Fiction",
            "description": "A test book description",
            "date_of_first_publish": "2020-01-01",
            "cover_image_url": "https://example.com/cover.jpg"
        }
    )

    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def sample_book_with_volumes(client: AsyncClient, auth_headers: dict) -> dict:
    """
    Create a sample multi-volume book in the catalog.

    Args:
        client: Test HTTP client.
        auth_headers: Authorization headers.

    Returns:
        dict: Created book data with volume information.
    """
    response = await client.post(
        "/api/library/books",
        headers=auth_headers,
        json={
            "title": "Reformed Dogmatics",
            "author": "Herman Bavinck",
            "genre": "Theology",
            "description": "A comprehensive systematic theology",
            "date_of_first_publish": "2003-01-01",
            "cover_image_url": "https://example.com/cover2.jpg",
            "series_title": "Reformed Dogmatics",
            "volume_number": 2,
            "volume_title": "God and creation"
        }
    )

    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def user_book(client: AsyncClient, auth_headers: dict, sample_book: dict) -> dict:
    """
    Add a book to user's library.

    Args:
        client: Test HTTP client.
        auth_headers: Authorization headers.
        sample_book: Sample book data.

    Returns:
        dict: User book data.
    """
    response = await client.post(
        "/api/library/my-library",
        headers=auth_headers,
        json={
            "book_id": sample_book["id"]
        }
    )

    assert response.status_code == 201
    return response.json()
