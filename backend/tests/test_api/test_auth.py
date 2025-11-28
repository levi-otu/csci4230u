"""Tests for authentication API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient) -> None:
    """Test user registration."""
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient) -> None:
    """Test registration with duplicate username."""
    # Register first user
    await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test1@example.com",
            "password": "TestPassword123!"
        }
    )

    # Try to register with same username
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient) -> None:
    """Test user login."""
    # Register user
    await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    # Login
    response = await client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient) -> None:
    """Test login with invalid credentials."""
    response = await client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
