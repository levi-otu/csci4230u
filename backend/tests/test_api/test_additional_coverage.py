"""Additional tests to increase coverage."""
import pytest
from httpx import AsyncClient


async def register_user(client: AsyncClient, username: str, email: str) -> tuple[str, str]:
    """Register user and return token and user_id."""
    response = await client.post("/api/auth/register", json={
        "username": username,
        "email": email,
        "password": "ValidPass123!",
        "full_name": f"{username} User"
    })
    token = response.json()["access_token"]
    me = await client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    return token, me.json()["id"]


@pytest.mark.asyncio
async def test_create_multiple_reading_lists_same_user(client: AsyncClient) -> None:
    """Test creating multiple reading lists for same user."""
    token, _ = await register_user(client, "multilist1", "ml1@example.com")

    for i in range(10):
        response = await client.post(
            "/api/library/reading-lists",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": f"List {i}", "description": f"Description {i}"}
        )
        assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_reading_list_by_id(client: AsyncClient) -> None:
    """Test getting reading list by ID."""
    token, _ = await register_user(client, "getlist", "getlist@example.com")

    # Create a list
    create_response = await client.post(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test List"}
    )
    list_id = create_response.json()["id"]

    # Get the list
    get_response = await client.get(
        f"/api/library/reading-lists/{list_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == "Test List"


@pytest.mark.asyncio
async def test_create_reading_list_minimal(client: AsyncClient) -> None:
    """Test creating reading list with minimal data."""
    token, _ = await register_user(client, "minimal", "minimal@example.com")

    response = await client.post(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Minimal"}
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_reading_list_name(client: AsyncClient) -> None:
    """Test updating reading list name."""
    token, _ = await register_user(client, "updname", "updname@example.com")

    # Create
    create_response = await client.post(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Original Name"}
    )
    list_id = create_response.json()["id"]

    # Update name only
    update_response = await client.patch(
        f"/api/library/reading-lists/{list_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "New Name"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "New Name"


@pytest.mark.asyncio
async def test_delete_reading_list_simple(client: AsyncClient) -> None:
    """Test deleting reading list."""
    token, _ = await register_user(client, "dellist", "dellist@example.com")

    # Create
    create_response = await client.post(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "To Delete"}
    )
    list_id = create_response.json()["id"]

    # Delete
    delete_response = await client.delete(
        f"/api/library/reading-lists/{list_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_get_empty_library_stats(client: AsyncClient) -> None:
    """Test library stats with no books."""
    token, _ = await register_user(client, "emptystats2", "es2@example.com")

    response = await client.get(
        "/api/library/stats",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_books"] == 0


@pytest.mark.asyncio
async def test_create_club_simple(client: AsyncClient) -> None:
    """Test simple club creation."""
    token, _ = await register_user(client, "clubmaker", "clubmaker@example.com")

    response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Simple Club"}
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_club_with_all_fields(client: AsyncClient) -> None:
    """Test club creation with all fields."""
    token, _ = await register_user(client, "fullclub", "fullclub@example.com")

    response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Full Club",
            "description": "A full description",
            "topic": "Books",
            "max_members": 100
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Full Club"
    assert data["description"] == "A full description"


@pytest.mark.asyncio
async def test_get_all_clubs(client: AsyncClient) -> None:
    """Test getting all clubs."""
    token, _ = await register_user(client, "allclubs", "allclubs@example.com")

    # Create a few clubs
    for i in range(3):
        await client.post(
            "/api/clubs",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": f"Club {i}"}
        )

    # Get all
    response = await client.get(
        "/api/clubs",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    clubs = response.json()
    assert len(clubs) >= 3


@pytest.mark.asyncio
async def test_get_club_by_id(client: AsyncClient) -> None:
    """Test getting club by ID."""
    token, _ = await register_user(client, "getclub", "getclub@example.com")

    # Create
    create_response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Get Club"}
    )
    club_id = create_response.json()["id"]

    # Get
    get_response = await client.get(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Get Club"


@pytest.mark.asyncio
async def test_update_club_name(client: AsyncClient) -> None:
    """Test updating club name."""
    token, _ = await register_user(client, "updclub", "updclub@example.com")

    # Create
    create_response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Original Club"}
    )
    club_id = create_response.json()["id"]

    # Update
    update_response = await client.patch(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Updated Club"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Club"


@pytest.mark.asyncio
async def test_delete_club_simple(client: AsyncClient) -> None:
    """Test deleting club."""
    token, _ = await register_user(client, "delclub", "delclub@example.com")

    # Create
    create_response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "To Delete"}
    )
    club_id = create_response.json()["id"]

    # Delete
    delete_response = await client.delete(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_add_member_to_club(client: AsyncClient) -> None:
    """Test adding member to club."""
    owner_token, _ = await register_user(client, "owner3", "owner3@example.com")
    member_token, member_id = await register_user(client, "member3", "member3@example.com")

    # Create club
    create_response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"name": "Member Club"}
    )
    club_id = create_response.json()["id"]

    # Add member
    add_response = await client.post(
        f"/api/clubs/{club_id}/members",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"user_id": member_id}
    )
    assert add_response.status_code == 201


@pytest.mark.asyncio
async def test_get_club_members_list(client: AsyncClient) -> None:
    """Test getting club members list."""
    token, _ = await register_user(client, "memberlist", "ml@example.com")

    # Create club
    create_response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Members Club"}
    )
    club_id = create_response.json()["id"]

    # Get members
    members_response = await client.get(
        f"/api/clubs/{club_id}/members",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert members_response.status_code == 200
    assert isinstance(members_response.json(), list)


@pytest.mark.asyncio
async def test_remove_member_from_club(client: AsyncClient) -> None:
    """Test removing member from club."""
    owner_token, _ = await register_user(client, "remowner", "remowner@example.com")
    member_token, member_id = await register_user(client, "remmember", "remmember@example.com")

    # Create club
    create_response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"name": "Remove Club"}
    )
    club_id = create_response.json()["id"]

    # Add member
    await client.post(
        f"/api/clubs/{club_id}/members",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"user_id": member_id}
    )

    # Remove member
    remove_response = await client.delete(
        f"/api/clubs/{club_id}/members/{member_id}",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert remove_response.status_code == 204


@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient) -> None:
    """Test getting all users."""
    token, _ = await register_user(client, "allusers", "allusers@example.com")

    response = await client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient) -> None:
    """Test getting user by ID."""
    token, user_id = await register_user(client, "getuser", "getuser@example.com")

    response = await client.get(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == user_id


@pytest.mark.asyncio
async def test_update_user_full_name(client: AsyncClient) -> None:
    """Test updating user full name."""
    token, user_id = await register_user(client, "upduser", "upduser@example.com")

    response = await client.patch(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "Updated Name"}
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"
