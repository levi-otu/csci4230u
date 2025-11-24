"""Tests for club API endpoints."""
import pytest
from httpx import AsyncClient
from uuid import uuid4


async def get_auth_token(
    client: AsyncClient,
    username: str = "testuser",
    email: str = "test@example.com",
    password: str = "testpassword123"
) -> str:
    """Helper to get authentication token."""
    response = await client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )
    return response.json()["access_token"]


async def get_user_id_from_token(
    client: AsyncClient,
    token: str
) -> str:
    """Helper to extract user ID from token by calling a protected endpoint."""
    response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()["id"]


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
    assert "id" in data
    assert "created_by" in data


@pytest.mark.asyncio
async def test_get_clubs(client: AsyncClient) -> None:
    """Test getting list of clubs."""
    token = await get_auth_token(client, "user1", "user1@example.com")

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
async def test_get_club_by_id(client: AsyncClient) -> None:
    """Test getting a specific club by ID."""
    token = await get_auth_token(client, "user2", "user2@example.com")

    # Create a club
    create_response = await client.post(
        "/api/clubs",
        json={
            "name": "Specific Club",
            "description": "Testing get by ID",
            "topic": "Mystery"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    club_id = create_response.json()["id"]

    # Get the club by ID
    response = await client.get(f"/api/clubs/{club_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == club_id
    assert data["name"] == "Specific Club"


@pytest.mark.asyncio
async def test_update_club(client: AsyncClient) -> None:
    """Test updating a club."""
    token = await get_auth_token(client, "user3", "user3@example.com")

    # Create a club
    create_response = await client.post(
        "/api/clubs",
        json={
            "name": "Original Name",
            "description": "Original Description",
            "topic": "Fiction"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    club_id = create_response.json()["id"]

    # Update the club
    response = await client.put(
        f"/api/clubs/{club_id}",
        json={
            "name": "Updated Name",
            "description": "Updated Description"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated Description"


@pytest.mark.asyncio
async def test_delete_club(client: AsyncClient) -> None:
    """Test deleting a club."""
    token = await get_auth_token(client, "user4", "user4@example.com")

    # Create a club
    create_response = await client.post(
        "/api/clubs",
        json={
            "name": "Club to Delete",
            "description": "This will be deleted",
            "topic": "Fiction"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    club_id = create_response.json()["id"]

    # Delete the club
    response = await client.delete(
        f"/api/clubs/{club_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # Verify club is deleted
    get_response = await client.get(f"/api/clubs/{club_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_add_user_to_club(client: AsyncClient) -> None:
    """Test adding a user to a club."""
    # Create owner and member users
    owner_token = await get_auth_token(
        client, "owner", "owner@example.com"
    )
    member_token = await get_auth_token(
        client, "member", "member@example.com"
    )
    member_user_id = await get_user_id_from_token(client, member_token)

    # Create a club
    create_response = await client.post(
        "/api/clubs",
        json={
            "name": "Membership Test Club",
            "description": "Testing memberships",
            "topic": "Fiction"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    club_id = create_response.json()["id"]

    # Add member to club
    response = await client.post(
        f"/api/clubs/{club_id}/members",
        json={
            "user_id": member_user_id,
            "role": "member"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == member_user_id
    assert data["club_id"] == club_id
    assert data["role"] == "member"
    assert "join_date" in data


@pytest.mark.asyncio
async def test_get_club_members(client: AsyncClient) -> None:
    """Test getting all members of a club."""
    # Create owner and members
    owner_token = await get_auth_token(
        client, "owner2", "owner2@example.com"
    )
    member1_token = await get_auth_token(
        client, "member1", "member1@example.com"
    )
    member2_token = await get_auth_token(
        client, "member2", "member2@example.com"
    )
    member1_id = await get_user_id_from_token(client, member1_token)
    member2_id = await get_user_id_from_token(client, member2_token)

    # Create a club
    create_response = await client.post(
        "/api/clubs",
        json={
            "name": "Members Test Club",
            "description": "Testing get members",
            "topic": "Science"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    club_id = create_response.json()["id"]

    # Add members
    await client.post(
        f"/api/clubs/{club_id}/members",
        json={"user_id": member1_id, "role": "member"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    await client.post(
        f"/api/clubs/{club_id}/members",
        json={"user_id": member2_id, "role": "member"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    # Get club members
    response = await client.get(f"/api/clubs/{club_id}/members")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    user_ids = [member["user_id"] for member in data]
    assert member1_id in user_ids
    assert member2_id in user_ids


@pytest.mark.asyncio
async def test_get_user_clubs(client: AsyncClient) -> None:
    """Test getting all clubs a user is a member of."""
    # Create users
    owner_token = await get_auth_token(
        client, "owner3", "owner3@example.com"
    )
    member_token = await get_auth_token(
        client, "member3", "member3@example.com"
    )
    member_id = await get_user_id_from_token(client, member_token)

    # Create two clubs
    club1_response = await client.post(
        "/api/clubs",
        json={
            "name": "Club 1",
            "description": "First club",
            "topic": "Fiction"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    club1_id = club1_response.json()["id"]

    club2_response = await client.post(
        "/api/clubs",
        json={
            "name": "Club 2",
            "description": "Second club",
            "topic": "Mystery"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    club2_id = club2_response.json()["id"]

    # Add member to both clubs
    await client.post(
        f"/api/clubs/{club1_id}/members",
        json={"user_id": member_id, "role": "member"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    await client.post(
        f"/api/clubs/{club2_id}/members",
        json={"user_id": member_id, "role": "member"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    # Get user's clubs
    response = await client.get(f"/api/clubs/user/{member_id}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    club_ids = [club["id"] for club in data]
    assert club1_id in club_ids
    assert club2_id in club_ids


@pytest.mark.asyncio
async def test_add_duplicate_member(client: AsyncClient) -> None:
    """Test adding the same user to a club twice fails."""
    owner_token = await get_auth_token(
        client, "owner4", "owner4@example.com"
    )
    member_token = await get_auth_token(
        client, "member4", "member4@example.com"
    )
    member_id = await get_user_id_from_token(client, member_token)

    # Create a club
    create_response = await client.post(
        "/api/clubs",
        json={
            "name": "Duplicate Test Club",
            "description": "Testing duplicates",
            "topic": "Fiction"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    club_id = create_response.json()["id"]

    # Add member once
    await client.post(
        f"/api/clubs/{club_id}/members",
        json={"user_id": member_id, "role": "member"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    # Try to add the same member again
    response = await client.post(
        f"/api/clubs/{club_id}/members",
        json={"user_id": member_id, "role": "member"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )

    assert response.status_code == 400
    assert "already a member" in response.json()["detail"]


@pytest.mark.asyncio
async def test_max_members_limit(client: AsyncClient) -> None:
    """Test that club respects max_members limit."""
    owner_token = await get_auth_token(
        client, "owner5", "owner5@example.com"
    )
    member1_token = await get_auth_token(
        client, "member5", "member5@example.com"
    )
    member2_token = await get_auth_token(
        client, "member6", "member6@example.com"
    )
    member1_id = await get_user_id_from_token(client, member1_token)
    member2_id = await get_user_id_from_token(client, member2_token)

    # Create a club with max_members = 1
    create_response = await client.post(
        "/api/clubs",
        json={
            "name": "Limited Club",
            "description": "Testing max members",
            "topic": "Fiction",
            "max_members": 1
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    club_id = create_response.json()["id"]

    # Add first member (should succeed)
    response1 = await client.post(
        f"/api/clubs/{club_id}/members",
        json={"user_id": member1_id, "role": "member"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert response1.status_code == 201

    # Try to add second member (should fail)
    response2 = await client.post(
        f"/api/clubs/{club_id}/members",
        json={"user_id": member2_id, "role": "member"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert response2.status_code == 400
    assert "maximum capacity" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_unauthorized_add_member(client: AsyncClient) -> None:
    """Test that non-owners cannot add members to a club."""
    owner_token = await get_auth_token(
        client, "owner6", "owner6@example.com"
    )
    non_owner_token = await get_auth_token(
        client, "nonowner", "nonowner@example.com"
    )
    member_token = await get_auth_token(
        client, "member7", "member7@example.com"
    )
    member_id = await get_user_id_from_token(client, member_token)

    # Create a club
    create_response = await client.post(
        "/api/clubs",
        json={
            "name": "Auth Test Club",
            "description": "Testing authorization",
            "topic": "Fiction"
        },
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    club_id = create_response.json()["id"]

    # Try to add member as non-owner
    response = await client.post(
        f"/api/clubs/{club_id}/members",
        json={"user_id": member_id, "role": "member"},
        headers={"Authorization": f"Bearer {non_owner_token}"}
    )

    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]


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


@pytest.mark.asyncio
async def test_get_nonexistent_club(client: AsyncClient) -> None:
    """Test getting a club that doesn't exist."""
    fake_club_id = str(uuid4())
    response = await client.get(f"/api/clubs/{fake_club_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
