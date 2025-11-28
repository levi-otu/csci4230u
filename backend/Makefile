.PHONY: help setup install start-db create-db configure-env migrate test clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup          - Initial setup: install uv, PostgreSQL, and start services"
	@echo "  make install        - Install dependencies and setup development environment"
	@echo "  make start-db       - Start PostgreSQL service"
	@echo "  make create-db      - Create database and user (interactive)"
	@echo "  make configure-env  - Generate .env file template"
	@echo "  make migrate        - Run database migrations"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Clean up generated files"
	@echo "  make start          - Start the application server and PostgreSQL service"

# Step 1-3: Install uv, PostgreSQL, and start services
setup:
	@echo "=== Installing uv ==="
	@if ! command -v uv &> /dev/null; then \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "uv installed successfully"; \
	else \
		echo "uv is already installed"; \
	fi
	@echo ""
	@echo "=== Installing PostgreSQL ==="
	@if [ "$$(uname)" = "Linux" ]; then \
		if command -v apt-get &> /dev/null; then \
			sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib; \
		else \
			echo "Unsupported Linux distribution. Please install PostgreSQL manually."; \
			exit 1; \
		fi \
	elif [ "$$(uname)" = "Darwin" ]; then \
		if command -v brew &> /dev/null; then \
			brew install postgresql; \
		else \
			echo "Homebrew not found. Please install Homebrew first."; \
			exit 1; \
		fi \
	else \
		echo "Unsupported OS. Please install PostgreSQL manually."; \
		exit 1; \
	fi
	@echo ""
	@echo "=== Starting PostgreSQL ==="
	$(MAKE) start-db
	@echo ""
	@echo "=== Setup Complete ==="
	@echo "Next steps:"
	@echo "  1. Run 'make create-db' to create the database and user"
	@echo "  2. Run 'make install' to install dependencies and setup environment"

# Start PostgreSQL service
start-db:
	@if [ "$$(uname)" = "Linux" ]; then \
		sudo service postgresql start; \
		echo "PostgreSQL started (Linux)"; \
	elif [ "$$(uname)" = "Darwin" ]; then \
		brew services start postgresql; \
		echo "PostgreSQL started (macOS)"; \
	fi

# Step 4: Create database and user (interactive)
create-db:
	@echo "=== Creating Database and User ==="
	@echo "You will be prompted to enter PostgreSQL console commands."
	@echo ""
	@echo "Please run the following commands in the PostgreSQL console:"
	@echo ""
	@echo "  CREATE DATABASE public_square;"
	@echo "  CREATE USER your_user WITH PASSWORD 'your_password';"
	@echo "  GRANT ALL PRIVILEGES ON DATABASE public_square TO your_user;"
	@echo "  CREATE DATABASE public_square_test;"
	@echo "  GRANT ALL PRIVILEGES ON DATABASE public_square_test TO your_user;"
	@echo "  \\q"
	@echo ""
	@sudo -u postgres psql

# Step 5-7: Install dependencies, configure environment, and run migrations
install:
	@echo "=== Installing Dependencies ==="
	uv sync
	@echo ""
	@echo "=== Configuring Environment ==="
	@if [ ! -f .env ]; then \
		$(MAKE) configure-env; \
	else \
		echo ".env file already exists. Skipping..."; \
		echo "If you need to regenerate it, run 'make configure-env'"; \
	fi
	@echo ""
	@echo "=== Running Database Migrations ==="
	@if [ -f .env ]; then \
		$(MAKE) migrate; \
	else \
		echo "⚠️  .env file not configured. Please update .env with your database credentials."; \
		echo "Then run 'make migrate' to apply database migrations."; \
	fi
	@echo ""
	@echo "=== Installation Complete ==="
	@echo "Your development environment is ready!"

# Generate .env file with template
configure-env:
	@echo "Generating .env file..."
	@SECRET_KEY=$$(openssl rand -hex 32); \
	echo "DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/public_square" > .env; \
	echo "TEST_DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/public_square_test" >> .env; \
	echo "SECRET_KEY=$$SECRET_KEY" >> .env
	@echo "✓ .env file created with generated SECRET_KEY"
	@echo "⚠️  Please update DATABASE_URL and TEST_DATABASE_URL with your actual credentials"

# Run database migrations
migrate:
	@echo "Generating migration..."
	@uv run alembic revision --autogenerate -m "Initial migration" || echo "Migration may already exist"
	@echo "Applying migrations..."
	uv run alembic upgrade head
	@echo "✓ Migrations applied"

# Run tests
test:
	uv run pytest

# Clean up
clean:
	@echo "Cleaning up..."
	@rm -rf .venv __pycache__ .pytest_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "✓ Cleanup complete"

start:
	sudo service postgresql start
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: psql
psql:
	PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d public_square