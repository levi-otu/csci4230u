"""Comprehensive library API tests for existing endpoints."""
import pytest
from httpx import AsyncClient


async def register_user(client: AsyncClient, username: str, email: str) -> tuple[str, str]:
    """Register a user and return token and user_id."""
    response = await client.post("/api/auth/register", json={
        "username": username,
        "email": email,
        "password": "TestPass123!",
        "full_name": f"{username} User"
    })
    token = response.json()["access_token"]

    me_response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    user_id = me_response.json()["id"]
    return token, user_id


@pytest.mark.asyncio
async def test_get_library_stats(client: AsyncClient) -> None:
    """Test getting library stats."""
    token, _ = await register_user(client, "statsuser", "stats@example.com")

    response = await client.get(
        "/api/library/stats",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_books" in data
    assert "read_books" in data
    assert "unread_books" in data


@pytest.mark.asyncio
async def test_get_reading_lists(client: AsyncClient) -> None:
    """Test getting all reading lists."""
    token, _ = await register_user(client, "listuser", "list@example.com")

    response = await client.get(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_reading_list(client: AsyncClient) -> None:
    """Test creating a reading list."""
    token, _ = await register_user(client, "createlist", "createlist@example.com")

    response = await client.post(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "My List",
            "description": "Test list"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My List"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user_books(client: AsyncClient) -> None:
    """Test getting user's library books."""
    token, _ = await register_user(client, "booksuser", "books@example.com")

    response = await client.get(
        "/api/library/books",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_reading_list_crud(client: AsyncClient) -> None:
    """Test full CRUD on reading lists."""
    token, _ = await register_user(client, "crudlist", "crudlist@example.com")

    # Create
    create_response = await client.post(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "CRUD List"}
    )
    assert create_response.status_code == 201
    list_id = create_response.json()["id"]

    # Read
    get_response = await client.get(
        f"/api/library/reading-lists/{list_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200

    # Update
    update_response = await client.patch(
        f"/api/library/reading-lists/{list_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Updated CRUD List"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated CRUD List"

    # Delete
    delete_response = await client.delete(
        f"/api/library/reading-lists/{list_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_multiple_reading_lists(client: AsyncClient) -> None:
    """Test creating multiple reading lists."""
    token, _ = await register_user(client, "multilists", "multi@example.com")

    list_ids = []
    for i in range(3):
        response = await client.post(
            "/api/library/reading-lists",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": f"List {i+1}"}
        )
        assert response.status_code == 201
        list_ids.append(response.json()["id"])

    # Get all lists
    get_response = await client.get(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    lists = get_response.json()
    assert len(lists) >= 3


@pytest.mark.asyncio
async def test_reading_list_with_description(client: AsyncClient) -> None:
    """Test creating reading list with description."""
    token, _ = await register_user(client, "desclist", "desc@example.com")

    response = await client.post(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Described List",
            "description": "This is a detailed description"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "This is a detailed description"


@pytest.mark.asyncio
async def test_update_reading_list_description(client: AsyncClient) -> None:
    """Test updating reading list description."""
    token, _ = await register_user(client, "updatedesc", "updatedesc@example.com")

    # Create
    create_response = await client.post(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Original"}
    )
    list_id = create_response.json()["id"]

    # Update description
    update_response = await client.patch(
        f"/api/library/reading-lists/{list_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "New description"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["description"] == "New description"


@pytest.mark.asyncio
async def test_library_stats_empty(client: AsyncClient) -> None:
    """Test library stats with no books."""
    token, _ = await register_user(client, "emptystats", "empty@example.com")

    response = await client.get(
        "/api/library/stats",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_books"] == 0
    assert data["read_books"] == 0


@pytest.mark.asyncio
async def test_get_empty_library(client: AsyncClient) -> None:
    """Test getting empty library."""
    token, _ = await register_user(client, "emptylib", "emptylib@example.com")

    response = await client.get(
        "/api/library/books",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_empty_reading_lists(client: AsyncClient) -> None:
    """Test getting empty reading lists."""
    token, _ = await register_user(client, "emptylists", "emptylists@example.com")

    response = await client.get(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == []
