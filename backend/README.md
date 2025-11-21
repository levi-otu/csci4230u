# Public Square API - FastAPI Backend

FastAPI backend for The Public Square book club application.

## Features

- **FastAPI Framework** - Modern, fast async web framework
- **PostgreSQL Database** - Async database operations with asyncpg
- **SQLAlchemy ORM** - Type-safe database models and relationships
- **Alembic Migrations** - Database schema version control
- **JWT Authentication** - Secure token-based authentication
- **Pydantic Validation** - Request/response validation
- **Storage Pattern** - Clean separation of data access
- **Pytest Testing** - Comprehensive test suite with 80% coverage target
- **PEP 8 Compliant** - Follows Python coding standards

## Project Structure

```
backend/
├── src/                          # Main application code
│   ├── api/                      # API route definitions
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── clubs.py             # Club endpoints (implemented)
│   │   ├── meetings.py          # Meeting endpoints (TODO)
│   │   ├── pages.py             # Page endpoints (TODO)
│   │   ├── books.py             # Book endpoints (TODO)
│   │   └── users.py             # User endpoints (TODO)
│   ├── handlers/                 # Business logic layer
│   │   ├── users/               # User handlers
│   │   │   └── auth_handler.py  # Auth business logic
│   │   └── clubs/               # Club handlers
│   │       └── club_handler.py  # Club business logic
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── user.py              # User, UserSecurity
│   │   ├── club.py              # Club, ClubMeeting
│   │   ├── meeting.py           # Meeting
│   │   ├── page.py              # Page
│   │   ├── book.py              # Book, BookVersion, Publisher
│   │   ├── group.py             # Group
│   │   └── role.py              # Role (RBAC)
│   ├── storage/data/sql/         # Data access layer
│   │   ├── base_repository.py   # Generic CRUD operations
│   │   ├── user_repository.py
│   │   ├── club_repository.py
│   │   ├── meeting_repository.py
│   │   ├── page_repository.py
│   │   └── book_repository.py
│   ├── transports/json/          # Request/response schemas
│   │   ├── auth_schemas.py
│   │   ├── user_schemas.py
│   │   ├── club_schemas.py
│   │   ├── meeting_schemas.py
│   │   ├── page_schemas.py
│   │   └── book_schemas.py
│   ├── config.py                 # Configuration settings
│   ├── database.py               # Database session & engine
│   ├── security.py               # JWT & password hashing
│   └── main.py                   # FastAPI app entry point
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest fixtures
│   ├── test_api/                # API endpoint tests
│   ├── test_handlers/           # Handler tests
│   └── test_storage/            # Storage tests
├── alembic/                      # Database migrations
├── .env                          # Environment variables
├── alembic.ini                   # Alembic configuration
├── pyproject.toml                # Project dependencies
└── pytest.ini                    # Pytest configuration
```

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- uv (Python package manager)

## Setup Instructions

### 1. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
```

### 3. Start PostgreSQL

**Ubuntu/Debian:**
```bash
sudo service postgresql start
```

**macOS:**
```bash
brew services start postgresql
```

### 4. Create Database and User

```bash
sudo -u postgres psql
```

In the PostgreSQL console:
```sql
CREATE DATABASE public_square;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE public_square TO your_user;

-- For test database
CREATE DATABASE public_square_test;
GRANT ALL PRIVILEGES ON DATABASE public_square_test TO your_user;

\q
```

### 5. Configure Environment Variables

Update [.env](.env) file with your database credentials:

```env
DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/public_square
TEST_DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/public_square_test
SECRET_KEY=your-secret-key-change-in-production
```

Generate a secure secret key:
```bash
openssl rand -hex 32
```

### 6. Install Dependencies

```bash
uv sync
```

### 7. Run Database Migrations

```bash
# Generate initial migration
uv run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
uv run alembic upgrade head
```

## Running the Application

### Development Server

```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

### Using uv shell (Optional)

```bash
uv shell
uvicorn src.main:app --reload
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Clubs (Implemented)

- `POST /api/clubs` - Create club (protected)
- `GET /api/clubs` - List clubs
- `GET /api/clubs/{id}` - Get club by ID
- `PUT /api/clubs/{id}` - Update club (protected)
- `DELETE /api/clubs/{id}` - Delete club (protected)

### Other Endpoints (TODO)

- Meetings: `/api/meetings`
- Pages: `/api/pages`
- Books: `/api/books`
- Users: `/api/users`

## Testing

### Run All Tests

```bash
uv run pytest
```

### Run with Coverage

```bash
uv run pytest --cov=src --cov-report=html
```

View coverage report: `open htmlcov/index.html`

### Run Specific Tests

```bash
# Run only API tests
uv run pytest tests/test_api/

# Run only auth tests
uv run pytest tests/test_api/test_auth.py

# Run specific test function
uv run pytest tests/test_api/test_auth.py::test_register_user
```

### Run with Markers

```bash
# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration
```

## Code Quality

### Linting with Flake8

```bash
uv run flake8 src tests
```

### Format Code (if black is added)

```bash
uv run black src tests
```

## Database Migrations

### Create a New Migration

```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
uv run alembic upgrade head
```

### Rollback Migration

```bash
uv run alembic downgrade -1
```

### View Migration History

```bash
uv run alembic history
```

### Check Current Version

```bash
uv run alembic current
```

## Development Workflow

1. **Create a new branch** for your feature
2. **Write tests** for new functionality
3. **Implement the feature** following PEP 8
4. **Run tests** and ensure 80% coverage
5. **Create migration** if database changes are needed
6. **Test locally** with the development server
7. **Submit pull request** for review

## Adding New Endpoints

To add new endpoints (e.g., for meetings, pages, books):

1. **Create handler** in `src/handlers/{entity}/{entity}_handler.py`
2. **Implement business logic** using the repository pattern
3. **Create API routes** in `src/api/{entity}.py`
4. **Add tests** in `tests/test_api/test_{entity}.py`
5. **Update this README** with new endpoints

Example handlers and endpoints for **clubs** are fully implemented as reference.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `TEST_DATABASE_URL` | Test database connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |
| `APP_NAME` | Application name | Public Square API |
| `DEBUG` | Debug mode | False |
| `BACKEND_CORS_ORIGINS` | Allowed CORS origins | [] |

## Troubleshooting

### Database Connection Issues

If you get connection errors:
1. Ensure PostgreSQL is running: `sudo service postgresql status`
2. Check credentials in `.env` file
3. Verify database exists: `psql -U your_user -d public_square`

### Migration Issues

If migrations fail:
1. Check database connection
2. Ensure all models are imported in `alembic/env.py`
3. Drop and recreate test database if needed

### Import Errors

If you get module import errors:
1. Ensure you're in the backend directory
2. Use `uv run` prefix for commands
3. Check Python version: `python --version` (should be 3.10+)

## Next Steps

- [ ] Implement remaining handlers (meetings, pages, books, users)
- [ ] Add RBAC (Role-Based Access Control) for permissions
- [ ] Implement WebRTC for video meetings
- [ ] Add email verification for registration
- [ ] Implement refresh tokens
- [ ] Add rate limiting
- [ ] Add logging and monitoring
- [ ] Set up CI/CD pipeline
- [ ] Deploy to production

## Contributing

1. Follow PEP 8 style guide
2. Write comprehensive tests (80% coverage minimum)
3. Use type hints for all functions
4. Add docstrings to all public functions
5. Follow the existing project structure

## License

This project is part of the CSCI4230U course final project at Ontario Tech University.
