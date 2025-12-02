# Selenium Tests for Public Square Backend

## Overview

This directory contains Selenium end-to-end tests that verify the complete workflow of:
1. Creating a user account
2. Adding a book to the library using ISBN lookup (ISBN: 9781451664829)
3. Changing the book's reading status to 'finished' (read)

## Test Files

- **test_selenium_library.py** - Main Selenium test file containing:
  - `test_add_book_by_isbn_workflow()` - Complete workflow test
  - `test_selenium_driver_works()` - Basic Selenium setup verification
  - `test_isbn_lookup_and_validation()` - ISBN lookup validation test

## Prerequisites

### 1. Install Dependencies

This project uses `uv` for dependency management. Install the required packages:

```bash
# Using uv (recommended for this project)
uv pip install selenium webdriver-manager

# Or using pip if not using uv
pip install -e ".[dev]"

# Or install manually
pip install selenium webdriver-manager requests
```

### 2. Chrome/Chromium Browser

The tests use Chrome in headless mode. Ensure Chrome or Chromium is installed:

```bash
# Check if Chrome is installed
which google-chrome

# Ubuntu/Debian
sudo apt-get install google-chrome-stable
# Or Chromium
sudo apt-get install chromium-browser
```

### 3. Environment Setup

Ensure your `.env` file is configured with test database settings:

```
TEST_DATABASE_URL=postgresql+asyncpg://user:pass@localhost/test_db
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dev_db
SECRET_KEY=your-secret-key
```

## Running the Tests

### Using Makefile (Recommended)

```bash
# Run all Selenium tests
make test-selenium

# Run all tests excluding Selenium (better coverage)
make test-no-selenium

# Run all tests
make test
```

### Using pytest Directly

```bash
# Run all selenium tests
pytest -m selenium -v

# Run with output
pytest -m selenium -v -s
```

### Run Specific Test

```bash
# Run only the main workflow test
pytest tests/test_selenium_library.py::test_add_book_by_isbn_workflow -v -s

# Run the driver verification test
pytest tests/test_selenium_library.py::test_selenium_driver_works -v -s

# Run the ISBN validation test
pytest tests/test_selenium_library.py::test_isbn_lookup_and_validation -v -s
```

### Run Without Coverage (Faster)

```bash
pytest -m selenium --no-cov -v -s
```

## Test Architecture

### Fixtures (from conftest.py)

1. **test_server** - Starts FastAPI server in background process
   - Runs on port 8001
   - Automatically cleaned up after test
   - Provides base URL to tests

2. **selenium_driver** - Creates Chrome WebDriver instance
   - Runs in headless mode
   - Configured with optimal settings for CI/CD
   - Automatic cleanup after test

### Test Flow

The main test (`test_add_book_by_isbn_workflow`) follows this flow:

```
1. Create User
   ├─> POST /api/auth/register
   └─> Receive access token

2. Lookup ISBN
   ├─> POST /api/library/books/lookup/isbn
   └─> Get book metadata for ISBN 9781451664829

3. Create Book in Catalog
   ├─> POST /api/library/books
   └─> Create book entry with ISBN data

4. Add to User Library
   ├─> POST /api/library/my-library
   └─> Add book to personal library (status: unread)

5. Change Reading Status
   ├─> POST /api/library/my-library/{id}/reading-status
   └─> Set status to 'finished' (read)

6. Verify Changes
   ├─> GET /api/library/my-library
   └─> Confirm book is marked as read
```

## CI/CD Integration

These tests are marked with `@pytest.mark.selenium` and `@pytest.mark.slow`, allowing you to:

```bash
# Skip selenium tests in regular runs
pytest -m "not selenium"

# Skip slow tests
pytest -m "not slow"

# Run only fast tests
pytest -m "not slow and not selenium"
```

## Troubleshooting

### Chrome Driver Issues

If you see "chromedriver" errors:
```bash
# The webdriver-manager should auto-download, but you can also:
pip install --upgrade webdriver-manager
```

### Server Already Running

If port 8001 is in use:
```bash
# Find and kill the process
lsof -ti:8001 | xargs kill -9
```

### Database Connection Issues

Ensure your test database is running:
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Create test database if needed
createdb test_public_square
```

## Expected Output

A successful test run should show:

```
[TEST] Step 1: Creating new user...
[TEST] User created successfully. Token: eyJhbGciOiJIUzI1NiIs...
[TEST] Step 2: Looking up book with ISBN 9781451664829...
[TEST] ISBN lookup result: {'found': True, 'title': 'The 7 Habits...'}
[TEST] Step 3: Creating book in catalog...
[TEST] Book created with ID: 12345678-1234-1234-1234-123456789abc
[TEST] Book title: The 7 Habits of Highly Effective People
[TEST] Book author: Stephen R. Covey
[TEST] Step 4: Adding book to user's library...
[TEST] Book added to library with user_book_id: 87654321-4321-4321-4321-abcdef123456
[TEST] Initial reading status: unread
[TEST] Step 5: Changing reading status to 'finished'...
[TEST] Reading status updated: finished
[TEST] Is read: True
[TEST] Read date: 2024-01-15T10:30:00
[TEST] Step 6: Verifying by fetching user's library...
[TEST] ✓ All assertions passed!
[TEST] Successfully created user, added book ISBN 9781451664829, and marked as read
```

## Notes

- Tests use the Open Library API for ISBN lookup (external dependency)
- If the external API is down, the ISBN lookup test will pass with a warning
- Each test creates a fresh user and database state
- Server starts fresh for each test function (function-scoped fixtures)
- Tests run in headless mode by default (no visible browser window)

## Book Information

**ISBN: 9781451664829**
- Title: The 7 Habits of Highly Effective People
- Author: Stephen R. Covey
- Genre: Self-Help / Business
- Published: 1989

This ISBN is used consistently across all tests for predictable results.
