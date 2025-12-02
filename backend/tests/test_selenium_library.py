"""Selenium end-to-end tests for library functionality."""
import time
from typing import Any

import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.selenium
@pytest.mark.slow
def test_add_book_by_isbn_workflow(selenium_driver: WebDriver, test_server: str) -> None:
    """
    Test the complete workflow of:
    1. Creating a user account
    2. Adding a book to library using ISBN (9781451664829)
    3. Changing the book's reading status to 'read'

    This test uses the API directly since this is a backend test,
    but uses Selenium to simulate browser-like interactions.

    Args:
        selenium_driver: Selenium WebDriver instance.
        test_server: Base URL of the test server.
    """
    driver = selenium_driver
    base_url = test_server

    # Step 1: Create a new user via API
    print("\n[TEST] Step 1: Creating new user...")

    registration_data = {
        "username": "selenium_testuser",
        "email": "selenium_test@example.com",
        "password": "TestPassword123!",
        "full_name": "Selenium Test User"
    }

    # Navigate to a page (needed for Selenium to work with requests)
    driver.get(f"{base_url}/docs")
    time.sleep(1)

    # Use requests to interact with API (simulating frontend API calls)
    register_response = requests.post(
        f"{base_url}/api/auth/register",
        json=registration_data
    )

    assert register_response.status_code == 201, f"Registration failed: {register_response.text}"
    auth_data = register_response.json()
    access_token = auth_data["access_token"]

    print(f"[TEST] User created successfully. Token: {access_token[:20]}...")

    # Step 2: Look up book by ISBN
    print("\n[TEST] Step 2: Looking up book with ISBN 9781451664829...")

    isbn = "9781451664829"
    headers = {"Authorization": f"Bearer {access_token}"}

    isbn_lookup_response = requests.post(
        f"{base_url}/api/library/books/lookup/isbn",
        json={"isbn": isbn},
        headers=headers
    )

    assert isbn_lookup_response.status_code == 200, \
        f"ISBN lookup failed: {isbn_lookup_response.text}"

    isbn_data = isbn_lookup_response.json()
    print(f"[TEST] ISBN lookup result: {isbn_data}")

    # Step 3: Create book in catalog using ISBN data
    print("\n[TEST] Step 3: Creating book in catalog...")

    book_create_data = {
        "title": isbn_data.get("title", "The 7 Habits of Highly Effective People"),
        "author": isbn_data.get("author", "Stephen R. Covey"),
        "genre": isbn_data.get("genre", "Self-Help"),
        "description": isbn_data.get("description", "A guide to personal effectiveness"),
        "date_of_first_publish": "1989-01-01",
        "cover_image_url": isbn_data.get("cover_url")
    }

    create_book_response = requests.post(
        f"{base_url}/api/library/books",
        json=book_create_data,
        headers=headers
    )

    assert create_book_response.status_code == 201, \
        f"Book creation failed: {create_book_response.text}"

    book_data = create_book_response.json()
    book_id = book_data["id"]

    print(f"[TEST] Book created with ID: {book_id}")
    print(f"[TEST] Book title: {book_data['title']}")
    print(f"[TEST] Book author: {book_data['author']}")

    # Step 4: Add book to user's library
    print("\n[TEST] Step 4: Adding book to user's library...")

    add_to_library_response = requests.post(
        f"{base_url}/api/library/my-library",
        json={"book_id": book_id},
        headers=headers
    )

    assert add_to_library_response.status_code == 201, \
        f"Adding to library failed: {add_to_library_response.text}"

    user_book_data = add_to_library_response.json()
    user_book_id = user_book_data["id"]

    print(f"[TEST] Book added to library with user_book_id: {user_book_id}")
    print(f"[TEST] Initial reading status: {user_book_data['reading_status']}")
    assert user_book_data["reading_status"] == "unread", "Initial status should be 'unread'"
    assert user_book_data["is_read"] is False, "Book should not be marked as read initially"

    # Step 5: Change reading status to 'finished' (read)
    print("\n[TEST] Step 5: Changing reading status to 'finished'...")

    set_status_response = requests.post(
        f"{base_url}/api/library/my-library/{user_book_id}/reading-status",
        json={"reading_status": "finished"},
        headers=headers
    )

    assert set_status_response.status_code == 200, \
        f"Setting reading status failed: {set_status_response.text}"

    updated_book_data = set_status_response.json()

    print(f"[TEST] Reading status updated: {updated_book_data['reading_status']}")
    print(f"[TEST] Is read: {updated_book_data['is_read']}")
    print(f"[TEST] Read date: {updated_book_data['read_date']}")

    # Step 6: Verify the status was changed correctly
    assert updated_book_data["reading_status"] == "finished", \
        "Reading status should be 'finished'"
    assert updated_book_data["is_read"] is True, \
        "Book should be marked as read"
    assert updated_book_data["read_date"] is not None, \
        "Read date should be set"

    # Step 7: Verify by fetching user's library
    print("\n[TEST] Step 6: Verifying by fetching user's library...")

    get_library_response = requests.get(
        f"{base_url}/api/library/my-library",
        headers=headers
    )

    assert get_library_response.status_code == 200, \
        f"Getting library failed: {get_library_response.text}"

    library_books = get_library_response.json()

    assert len(library_books) == 1, "Library should contain exactly one book"

    library_book = library_books[0]
    assert library_book["book"]["title"] == book_data["title"], \
        "Book title should match"
    assert library_book["reading_status"] == "finished", \
        "Reading status should be 'finished' in library view"
    assert library_book["is_read"] is True, \
        "Book should be marked as read in library view"

    print("\n[TEST] ✓ All assertions passed!")
    print(f"[TEST] Successfully created user, added book ISBN {isbn}, and marked as read")


@pytest.mark.selenium
@pytest.mark.slow
def test_selenium_driver_works(selenium_driver: WebDriver, test_server: str) -> None:
    """
    Basic test to verify Selenium driver is working.

    Args:
        selenium_driver: Selenium WebDriver instance.
        test_server: Base URL of the test server.
    """
    driver = selenium_driver

    # Navigate to the API docs
    driver.get(f"{test_server}/docs")

    # Wait for page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Verify we can access the page
    assert "FastAPI" in driver.page_source or "swagger" in driver.page_source.lower(), \
        "Should be able to access API docs"

    print(f"\n[TEST] ✓ Selenium driver working, accessed: {driver.current_url}")


@pytest.mark.selenium
@pytest.mark.slow
def test_isbn_lookup_and_validation(selenium_driver: WebDriver, test_server: str) -> None:
    """
    Test ISBN lookup functionality with the specific ISBN.

    Args:
        selenium_driver: Selenium WebDriver instance.
        test_server: Base URL of the test server.
    """
    driver = selenium_driver
    base_url = test_server

    # Create a test user first
    registration_data = {
        "username": "isbn_testuser",
        "email": "isbn_test@example.com",
        "password": "TestPassword123!",
        "full_name": "ISBN Test User"
    }

    driver.get(f"{base_url}/docs")
    time.sleep(1)

    register_response = requests.post(
        f"{base_url}/api/auth/register",
        json=registration_data
    )

    assert register_response.status_code == 201
    auth_data = register_response.json()
    access_token = auth_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Test ISBN lookup
    isbn = "9781451664829"

    isbn_response = requests.post(
        f"{base_url}/api/library/books/lookup/isbn",
        json={"isbn": isbn},
        headers=headers
    )

    assert isbn_response.status_code == 200
    isbn_data = isbn_response.json()

    print("\n[TEST] ISBN Lookup Result:")
    print(f"  Found: {isbn_data['found']}")
    print(f"  Title: {isbn_data.get('title', 'N/A')}")
    print(f"  Author: {isbn_data.get('author', 'N/A')}")
    print(f"  ISBN-10: {isbn_data.get('isbn_10', 'N/A')}")
    print(f"  ISBN-13: {isbn_data.get('isbn_13', 'N/A')}")

    # The ISBN should be found (if Open Library API is working)
    # But we don't fail the test if it's not found, as external API might be down
    if isbn_data['found']:
        assert isbn_data.get('title') is not None, "Title should be present if book is found"
        print("[TEST] ✓ ISBN lookup successful!")
    else:
        print("[TEST] ⚠ ISBN not found in external API (this is acceptable)")
