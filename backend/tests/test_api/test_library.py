"""Tests for library API endpoints."""
import pytest
from httpx import AsyncClient


# Book CRUD Tests

@pytest.mark.asyncio
async def test_create_book(client: AsyncClient, auth_headers: dict) -> None:
    """Test creating a book."""
    response = await client.post(
        "/api/library/books",
        headers=auth_headers,
        json={
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Fiction",
            "description": "A test book",
            "date_of_first_publish": "2020-01-01",
            "cover_image_url": "https://example.com/cover.jpg"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert data["genre"] == "Fiction"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_book_with_volumes(client: AsyncClient, auth_headers: dict) -> None:
    """Test creating a multi-volume book."""
    response = await client.post(
        "/api/library/books",
        headers=auth_headers,
        json={
            "title": "Reformed Dogmatics",
            "author": "Herman Bavinck",
            "genre": "Theology",
            "series_title": "Reformed Dogmatics",
            "volume_number": 2,
            "volume_title": "God and creation"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["series_title"] == "Reformed Dogmatics"
    assert data["volume_number"] == 2
    assert data["volume_title"] == "God and creation"


@pytest.mark.asyncio
async def test_create_book_missing_fields(client: AsyncClient, auth_headers: dict) -> None:
    """Test creating a book with missing required fields."""
    response = await client.post(
        "/api/library/books",
        headers=auth_headers,
        json={
            "title": "Test Book"
            # Missing author
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_book_unauthorized(client: AsyncClient) -> None:
    """Test creating a book without authentication."""
    response = await client.post(
        "/api/library/books",
        json={
            "title": "Test Book",
            "author": "Test Author"
        }
    )

    # FastAPI returns 403 (Forbidden) when authentication is missing
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_book(client: AsyncClient, auth_headers: dict, sample_book: dict) -> None:
    """Test getting a book by ID."""
    response = await client.get(
        f"/api/library/books/{sample_book['id']}",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_book["id"]
    assert data["title"] == sample_book["title"]


@pytest.mark.asyncio
async def test_get_book_not_found(client: AsyncClient, auth_headers: dict) -> None:
    """Test getting a non-existent book."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = await client.get(
        f"/api/library/books/{fake_uuid}",
        headers=auth_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_book(client: AsyncClient, auth_headers: dict, sample_book: dict) -> None:
    """Test updating a book."""
    response = await client.put(
        f"/api/library/books/{sample_book['id']}",
        headers=auth_headers,
        json={
            "title": "Updated Title",
            "author": "Updated Author"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["author"] == "Updated Author"


@pytest.mark.asyncio
async def test_update_book_add_volume_info(client: AsyncClient, auth_headers: dict, sample_book: dict) -> None:
    """Test adding volume information to an existing book."""
    response = await client.put(
        f"/api/library/books/{sample_book['id']}",
        headers=auth_headers,
        json={
            "series_title": "Test Series",
            "volume_number": 1,
            "volume_title": "Introduction"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["series_title"] == "Test Series"
    assert data["volume_number"] == 1
    assert data["volume_title"] == "Introduction"


@pytest.mark.asyncio
async def test_update_book_remove_volume_info(client: AsyncClient, auth_headers: dict, sample_book_with_volumes: dict) -> None:
    """Test removing volume information from a book."""
    response = await client.put(
        f"/api/library/books/{sample_book_with_volumes['id']}",
        headers=auth_headers,
        json={
            "series_title": None,
            "volume_number": None,
            "volume_title": None
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["series_title"] is None
    assert data["volume_number"] is None
    assert data["volume_title"] is None


@pytest.mark.asyncio
async def test_delete_book(client: AsyncClient, auth_headers: dict, sample_book: dict) -> None:
    """Test deleting a book."""
    response = await client.delete(
        f"/api/library/books/{sample_book['id']}",
        headers=auth_headers
    )

    assert response.status_code == 204

    # Verify book is deleted
    get_response = await client.get(
        f"/api/library/books/{sample_book['id']}",
        headers=auth_headers
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_search_books(client: AsyncClient, auth_headers: dict, sample_book: dict) -> None:
    """Test searching books."""
    # Search endpoint might not exist, skip for now
    pytest.skip("Search endpoint not implemented yet")


# User Library Tests

@pytest.mark.asyncio
async def test_add_to_library(client: AsyncClient, auth_headers: dict, sample_book: dict) -> None:
    """Test adding a book to user's library."""
    response = await client.post(
        "/api/library/my-library",
        headers=auth_headers,
        json={
            "book_id": sample_book["id"]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["book_id"] == sample_book["id"]
    assert data["reading_status"] == "unread"
    assert data["is_read"] is False
    assert data["is_favorite"] is False


@pytest.mark.asyncio
async def test_add_duplicate_to_library(client: AsyncClient, auth_headers: dict, sample_book: dict) -> None:
    """Test adding the same book twice."""
    # Add first time
    await client.post(
        "/api/library/my-library",
        headers=auth_headers,
        json={"book_id": sample_book["id"]}
    )

    # Try to add again
    response = await client.post(
        "/api/library/my-library",
        headers=auth_headers,
        json={"book_id": sample_book["id"]}
    )

    assert response.status_code == 400
    assert "already in" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_my_library(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test getting user's library."""
    response = await client.get(
        "/api/library/my-library",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == user_book["id"]


@pytest.mark.asyncio
async def test_get_my_library_with_filters(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test getting user's library with filters."""
    # Mark as read
    await client.post(
        f"/api/library/my-library/{user_book['id']}/reading-status",
        headers=auth_headers,
        json={"reading_status": "finished"}
    )

    # Filter by is_read
    response = await client.get(
        "/api/library/my-library",
        headers=auth_headers,
        params={"is_read": "true"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["is_read"] is True


@pytest.mark.asyncio
async def test_remove_from_library(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test removing a book from user's library."""
    response = await client.delete(
        f"/api/library/my-library/{user_book['id']}",
        headers=auth_headers
    )

    assert response.status_code == 204

    # Verify book is removed
    get_response = await client.get(
        "/api/library/my-library",
        headers=auth_headers
    )
    assert len(get_response.json()) == 0


# Reading Status Tests

@pytest.mark.asyncio
async def test_set_reading_status_to_reading(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test setting reading status to 'reading'."""
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/reading-status",
        headers=auth_headers,
        json={"reading_status": "reading"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reading_status"] == "reading"
    assert data["is_read"] is False
    assert data["read_date"] is None


@pytest.mark.asyncio
async def test_set_reading_status_to_finished(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test setting reading status to 'finished'."""
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/reading-status",
        headers=auth_headers,
        json={"reading_status": "finished"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reading_status"] == "finished"
    assert data["is_read"] is True
    assert data["read_date"] is not None


@pytest.mark.asyncio
async def test_set_reading_status_to_unread(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test setting reading status to 'unread'."""
    # First mark as finished
    await client.post(
        f"/api/library/my-library/{user_book['id']}/reading-status",
        headers=auth_headers,
        json={"reading_status": "finished"}
    )

    # Then mark as unread
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/reading-status",
        headers=auth_headers,
        json={"reading_status": "unread"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reading_status"] == "unread"
    assert data["is_read"] is False
    assert data["read_date"] is None


@pytest.mark.asyncio
async def test_set_invalid_reading_status(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test setting an invalid reading status."""
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/reading-status",
        headers=auth_headers,
        json={"reading_status": "invalid"}
    )

    # Should return 400 Bad Request or 422 for invalid status
    assert response.status_code in [400, 422]


# Rating and Review Tests

@pytest.mark.asyncio
async def test_add_rating(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test adding a rating to a book."""
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/rating",
        headers=auth_headers,
        json={"rating": 4.5}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 4.5


@pytest.mark.asyncio
async def test_add_invalid_rating(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test adding an invalid rating."""
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/rating",
        headers=auth_headers,
        json={"rating": 6.0}  # Rating should be 0-5
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_review(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test adding a review to a book."""
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/review",
        headers=auth_headers,
        json={"review": "Great book! Highly recommended."}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["review"] == "Great book! Highly recommended."


@pytest.mark.asyncio
async def test_add_notes(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test adding notes to a book."""
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/notes",
        headers=auth_headers,
        json={"notes": "Chapter 3 was particularly insightful."}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["notes"] == "Chapter 3 was particularly insightful."


# Favorite Tests

@pytest.mark.asyncio
async def test_toggle_favorite(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test toggling favorite status."""
    # Toggle on
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/toggle-favorite",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_favorite"] is True

    # Toggle off
    response = await client.post(
        f"/api/library/my-library/{user_book['id']}/toggle-favorite",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_favorite"] is False


# Update User Book Tests

@pytest.mark.asyncio
async def test_update_user_book(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test updating multiple user book fields at once."""
    response = await client.put(
        f"/api/library/my-library/{user_book['id']}",
        headers=auth_headers,
        json={
            "rating": 5.0,
            "review": "Amazing book!",
            "notes": "Must read again",
            "is_favorite": True
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5.0
    assert data["review"] == "Amazing book!"
    assert data["notes"] == "Must read again"
    assert data["is_favorite"] is True


# Library Statistics Tests

@pytest.mark.asyncio
async def test_get_library_stats(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test getting library statistics."""
    # Mark one book as read
    await client.post(
        f"/api/library/my-library/{user_book['id']}/reading-status",
        headers=auth_headers,
        json={"reading_status": "finished"}
    )

    response = await client.get(
        "/api/library/stats",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_books"] >= 1
    assert data["read_books"] >= 1


# ISBN Lookup Tests

@pytest.mark.asyncio
async def test_isbn_lookup_not_found(client: AsyncClient, auth_headers: dict) -> None:
    """Test ISBN lookup for a book that doesn't exist in Open Library."""
    # Use an ISBN that likely doesn't exist
    response = await client.post(
        "/api/library/books/lookup/isbn",
        headers=auth_headers,
        json={"isbn": "9999999999999"}
    )

    assert response.status_code == 200
    data = response.json()
    # Either not found, or if found, at least returns a response
    assert "found" in data


# Authorization Tests

@pytest.mark.asyncio
async def test_access_other_user_book(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test that users cannot access other users' books."""
    # Create another user
    await client.post(
        "/api/auth/register",
        json={
            "username": "otheruser",
            "email": "other@example.com",
            "password": "password123"
        }
    )

    # Login as other user
    login_response = await client.post(
        "/api/auth/login",
        json={
            "email": "other@example.com",
            "password": "password123"
        }
    )

    other_headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # Try to access first user's book
    response = await client.get(
        f"/api/library/my-library/{user_book['id']}",
        headers=other_headers
    )

    assert response.status_code == 404


# Reading List Tests

@pytest.mark.asyncio
async def test_create_reading_list(client: AsyncClient, auth_headers: dict) -> None:
    """Test creating a reading list."""
    response = await client.post(
        "/api/library/reading-lists",
        headers=auth_headers,
        json={
            "name": "Summer Reading",
            "description": "Books to read this summer"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Summer Reading"
    assert data["description"] == "Books to read this summer"


@pytest.mark.asyncio
async def test_get_reading_lists(client: AsyncClient, auth_headers: dict) -> None:
    """Test getting all reading lists."""
    # Create a list
    await client.post(
        "/api/library/reading-lists",
        headers=auth_headers,
        json={"name": "Test List"}
    )

    response = await client.get(
        "/api/library/reading-lists",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_add_book_to_reading_list(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test adding a book to a reading list."""
    # Create a list
    list_response = await client.post(
        "/api/library/reading-lists",
        headers=auth_headers,
        json={"name": "Test List"}
    )
    reading_list = list_response.json()

    # Add book to list
    response = await client.post(
        f"/api/library/reading-lists/{reading_list['id']}/items",
        headers=auth_headers,
        json={"user_book_id": user_book["id"]}
    )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_remove_book_from_reading_list(client: AsyncClient, auth_headers: dict, user_book: dict) -> None:
    """Test removing a book from a reading list."""
    # Create a list and add book
    list_response = await client.post(
        "/api/library/reading-lists",
        headers=auth_headers,
        json={"name": "Test List"}
    )
    reading_list = list_response.json()

    await client.post(
        f"/api/library/reading-lists/{reading_list['id']}/items",
        headers=auth_headers,
        json={"user_book_id": user_book["id"]}
    )

    # Remove book (use user_book_id directly)
    response = await client.delete(
        f"/api/library/reading-lists/{reading_list['id']}/items/{user_book['id']}",
        headers=auth_headers
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_reading_list(client: AsyncClient, auth_headers: dict) -> None:
    """Test deleting a reading list."""
    # Create a list
    list_response = await client.post(
        "/api/library/reading-lists",
        headers=auth_headers,
        json={"name": "Test List"}
    )
    reading_list = list_response.json()

    # Delete list
    response = await client.delete(
        f"/api/library/reading-lists/{reading_list['id']}",
        headers=auth_headers
    )

    assert response.status_code == 204
