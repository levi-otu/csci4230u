"""Tests for club API endpoints."""
import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient) -> str:
    """Helper to get authentication token."""
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_club(client: AsyncClient) -> None:
    """Test creating a club."""
    token = await get_auth_token(client)

    response = await client.post(
        "/api/clubs",
        json={
            "name": "Test Book Club",
            "description": "A club for testing",
            "topic": "Fiction",
            "max_members": 50
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Book Club"
    assert data["description"] == "A club for testing"
    assert data["topic"] == "Fiction"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_get_clubs(client: AsyncClient) -> None:
    """Test getting list of clubs."""
    token = await get_auth_token(client)

    # Create a club
    await client.post(
        "/api/clubs",
        json={
            "name": "Test Club",
            "description": "Test",
            "topic": "Fiction"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get clubs
    response = await client.get("/api/clubs")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_create_club_unauthorized(client: AsyncClient) -> None:
    """Test creating a club without authentication."""
    response = await client.post(
        "/api/clubs",
        json={
            "name": "Test Club",
            "description": "Test",
            "topic": "Fiction"
        }
    )

    assert response.status_code == 403
