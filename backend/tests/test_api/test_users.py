"""Tests for user API endpoints."""
import pytest
from httpx import AsyncClient


async def get_auth_token(
    client: AsyncClient,
    username: str = "testuser",
    email: str = "test@example.com",
    password: str = "TestPassword123!"
) -> tuple[str, str]:
    """Helper to get authentication token and user ID."""
    response = await client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "full_name": "Test User"
        }
    )
    data = response.json()
    # Get user ID by fetching user info
    me_response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {data['access_token']}"}
    )
    user_id = me_response.json()["id"]
    return data["access_token"], user_id


@pytest.mark.asyncio
async def test_update_user_full_name(client: AsyncClient) -> None:
    """Test updating user's full name."""
    token, user_id = await get_auth_token(client, "updateuser", "update@example.com")

    response = await client.put(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "Updated Tester"}
    )

    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Tester"


@pytest.mark.asyncio
async def test_update_user_not_found(client: AsyncClient) -> None:
    """Test updating a non-existent user."""
    token, _ = await get_auth_token(client, "user404", "user404@example.com")
    invalid_id = "00000000-0000-0000-0000-000000000000"

    response = await client.put(
        f"/api/users/{invalid_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "Nobody"}
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient) -> None:
    """Test deleting a user."""
    token, user_id = await get_auth_token(client, "deleteuser", "delete@example.com")

    response = await client.delete(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # Verify user is deleted
    get_response = await client.get(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404
