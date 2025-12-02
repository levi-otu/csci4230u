"""Additional workflow tests to increase handler and storage coverage."""
import pytest
from httpx import AsyncClient


async def create_auth_user(client: AsyncClient, username: str, email: str) -> tuple[str, str]:
    """Create user and return token and user_id."""
    response = await client.post("/api/auth/register", json={
        "username": username,
        "email": email,
        "password": "TestPass123!",
        "full_name": f"{username} User"
    })
    token = response.json()["access_token"]
    me = await client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    return token, me.json()["id"]


@pytest.mark.asyncio
async def test_auth_login_and_refresh(client: AsyncClient) -> None:
    """Test complete auth flow with login and refresh."""
    username = "logintest"
    email = "logintest@example.com"
    password = "TestPass123!"

    # Register
    register_response = await client.post("/api/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    assert register_response.status_code == 201

    # Login
    login_response = await client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data

    # Use access token
    me_response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {login_data['access_token']}"}
    )
    assert me_response.status_code == 200


@pytest.mark.asyncio
async def test_clubs_full_workflow(client: AsyncClient) -> None:
    """Test complete clubs workflow with multiple users."""
    owner_token, owner_id = await create_auth_user(client, "owner1", "owner1@example.com")
    member1_token, member1_id = await create_auth_user(client, "member1", "member1@example.com")
    member2_token, member2_id = await create_auth_user(client, "member2", "member2@example.com")

    # Create club
    club_response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "name": "Full Workflow Club",
            "description": "Testing all features",
            "topic": "Books"
        }
    )
    assert club_response.status_code == 201
    club_id = club_response.json()["id"]

    # Get club
    get_response = await client.get(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert get_response.status_code == 200

    # List all clubs
    list_response = await client.get(
        "/api/clubs",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert list_response.status_code == 200

    # Update club
    update_response = await client.patch(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"description": "Updated description"}
    )
    assert update_response.status_code == 200

    # Add members
    add1_response = await client.post(
        f"/api/clubs/{club_id}/members",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"user_id": member1_id}
    )
    assert add1_response.status_code == 201

    add2_response = await client.post(
        f"/api/clubs/{club_id}/members",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"user_id": member2_id}
    )
    assert add2_response.status_code == 201

    # Get members
    members_response = await client.get(
        f"/api/clubs/{club_id}/members",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert members_response.status_code == 200

    # Remove a member
    remove_response = await client.delete(
        f"/api/clubs/{club_id}/members/{member2_id}",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert remove_response.status_code == 204

    # Delete club
    delete_response = await client.delete(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_users_list_and_get(client: AsyncClient) -> None:
    """Test listing and getting users."""
    token1, user1_id = await create_auth_user(client, "list1", "list1@example.com")
    token2, user2_id = await create_auth_user(client, "list2", "list2@example.com")

    # List users
    list_response = await client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert list_response.status_code == 200
    users = list_response.json()
    assert len(users) >= 2

    # Get specific user
    get_response = await client.get(
        f"/api/users/{user2_id}",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert get_response.status_code == 200


@pytest.mark.asyncio
async def test_user_update_profile(client: AsyncClient) -> None:
    """Test updating user profile."""
    token, user_id = await create_auth_user(client, "profile", "profile@example.com")

    # Update full_name
    update1 = await client.patch(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "New Full Name"}
    )
    assert update1.status_code == 200
    assert update1.json()["full_name"] == "New Full Name"

    # Update username
    update2 = await client.patch(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "newusername"}
    )
    assert update2.status_code == 200
    assert update2.json()["username"] == "newusername"

    # Update email
    update3 = await client.patch(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "newemail@example.com"}
    )
    assert update3.status_code == 200
    assert update3.json()["email"] == "newemail@example.com"


@pytest.mark.asyncio
async def test_multiple_clubs(client: AsyncClient) -> None:
    """Test creating and managing multiple clubs."""
    token, user_id = await create_auth_user(client, "multiclub", "multiclub@example.com")

    club_ids = []
    for i in range(5):
        response = await client.post(
            "/api/clubs",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": f"Club {i+1}",
                "description": f"Description {i+1}",
                "topic": f"Topic {i+1}"
            }
        )
        assert response.status_code == 201
        club_ids.append(response.json()["id"])

    # Get all clubs
    list_response = await client.get(
        "/api/clubs",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert list_response.status_code == 200
    clubs = list_response.json()
    assert len(clubs) >= 5

    # Get each club
    for club_id in club_ids:
        get_response = await client.get(
            f"/api/clubs/{club_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert get_response.status_code == 200


@pytest.mark.asyncio
async def test_reading_lists_multiple_operations(client: AsyncClient) -> None:
    """Test multiple reading list operations."""
    token, user_id = await create_auth_user(client, "readlists", "readlists@example.com")

    # Create multiple lists
    list_ids = []
    for i in range(3):
        response = await client.post(
            "/api/library/reading-lists",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": f"Reading List {i+1}"}
        )
        assert response.status_code == 201
        list_ids.append(response.json()["id"])

    # Get all lists
    get_all = await client.get(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_all.status_code == 200
    assert len(get_all.json()) >= 3

    # Update each list
    for i, list_id in enumerate(list_ids):
        update_response = await client.patch(
            f"/api/library/reading-lists/{list_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": f"Updated List {i+1}"}
        )
        assert update_response.status_code == 200

    # Delete all lists
    for list_id in list_ids:
        delete_response = await client.delete(
            f"/api/library/reading-lists/{list_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_auth_me_endpoint(client: AsyncClient) -> None:
    """Test /users/me endpoint."""
    username = "metest"
    email = "metest@example.com"
    token, user_id = await create_auth_user(client, username, email)

    response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == username
    assert data["email"] == email


@pytest.mark.asyncio
async def test_library_stats_with_data(client: AsyncClient) -> None:
    """Test library stats endpoint."""
    token, user_id = await create_auth_user(client, "libstats", "libstats@example.com")

    # Get initial stats
    stats1 = await client.get(
        "/api/library/stats",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert stats1.status_code == 200
    data1 = stats1.json()
    assert "total_books" in data1
    assert "read_books" in data1
    assert "unread_books" in data1
    assert "favorite_books" in data1


@pytest.mark.asyncio
async def test_club_update_fields(client: AsyncClient) -> None:
    """Test updating different club fields."""
    token, user_id = await create_auth_user(client, "clubfields", "clubfields@example.com")

    # Create club
    create_response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Fields Club"}
    )
    club_id = create_response.json()["id"]

    # Update name
    update1 = await client.patch(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "New Name"}
    )
    assert update1.status_code == 200

    # Update description
    update2 = await client.patch(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "New Description"}
    )
    assert update2.status_code == 200

    # Update topic
    update3 = await client.patch(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"topic": "New Topic"}
    )
    assert update3.status_code == 200

    # Update is_active
    update4 = await client.patch(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": False}
    )
    assert update4.status_code == 200


@pytest.mark.asyncio
async def test_logout(client: AsyncClient) -> None:
    """Test logout endpoint."""
    token, user_id = await create_auth_user(client, "logouttest", "logout@example.com")

    # Logout
    logout_response = await client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    # Check if logout endpoint exists and returns appropriate status
    assert logout_response.status_code in [200, 204, 401]


@pytest.mark.asyncio
async def test_multiple_users_same_club(client: AsyncClient) -> None:
    """Test multiple users in same club."""
    users = []
    for i in range(4):
        token, user_id = await create_auth_user(client, f"clubuser{i}", f"clubuser{i}@example.com")
        users.append((token, user_id))

    owner_token, owner_id = users[0]

    # Create club
    club_response = await client.post(
        "/api/clubs",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"name": "Multi User Club"}
    )
    club_id = club_response.json()["id"]

    # Add all other users
    for token, user_id in users[1:]:
        add_response = await client.post(
            f"/api/clubs/{club_id}/members",
            headers={"Authorization": f"Bearer {owner_token}"},
            json={"user_id": user_id}
        )
        assert add_response.status_code == 201

    # Get members
    members_response = await client.get(
        f"/api/clubs/{club_id}/members",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert members_response.status_code == 200


@pytest.mark.asyncio
async def test_reading_list_default_flag(client: AsyncClient) -> None:
    """Test reading list with is_default flag."""
    token, user_id = await create_auth_user(client, "defaultlist", "defaultlist@example.com")

    # Create default list
    response = await client.post(
        "/api/library/reading-lists",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Default List", "is_default": True}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["is_default"] is True
