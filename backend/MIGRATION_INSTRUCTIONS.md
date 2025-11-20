# Database Migration Instructions

## Prerequisites

Before running migrations, ensure you have PostgreSQL installed and running.

### Setting up PostgreSQL

1. **Install PostgreSQL** (if not already installed):
   ```bash
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   ```

2. **Start PostgreSQL service**:
   ```bash
   sudo service postgresql start
   ```

3. **Create database and user**:
   ```bash
   sudo -u postgres psql
   ```

   Then in the PostgreSQL console:
   ```sql
   CREATE DATABASE public_square;
   CREATE USER your_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE public_square TO your_user;

   -- For test database
   CREATE DATABASE public_square_test;
   GRANT ALL PRIVILEGES ON DATABASE public_square_test TO your_user;

   \q
   ```

4. **Update .env file** with your database credentials:
   ```env
   DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/public_square
   TEST_DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/public_square_test
   ```

## Running Migrations

Once PostgreSQL is set up:

1. **Generate a new migration** (autogenerate from models):
   ```bash
   uv run alembic revision --autogenerate -m "Description of changes"
   ```

2. **Review the generated migration** in `alembic/versions/`

3. **Apply migrations** to the database:
   ```bash
   uv run alembic upgrade head
   ```

4. **Rollback a migration** (if needed):
   ```bash
   uv run alembic downgrade -1
   ```

5. **View migration history**:
   ```bash
   uv run alembic history
   ```

6. **Check current migration version**:
   ```bash
   uv run alembic current
   ```

## Initial Migration

The initial migration will create all tables:
- users
- user_security
- roles
- user_roles
- groups
- user_groups
- pages
- user_pages
- clubs
- user_clubs
- club_meetings
- meetings
- books
- book_versions
- publishers

After setting up PostgreSQL, run:
```bash
uv run alembic revision --autogenerate -m "Initial migration - create all tables"
uv run alembic upgrade head
```
