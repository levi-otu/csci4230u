FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_SYSTEM_PYTHON=1

# Install basic build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# ✅ uv is in /root/.local/bin, so add that to PATH
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install deps with uv into .venv (prod)
RUN uv sync --frozen --no-dev

# Copy the rest of the backend (exclude .venv to avoid overwriting the one we just created)
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY main.py ./main.py
COPY pytest.ini ./pytest.ini

# Use the venv by default
ENV VIRTUAL_ENV="/app/.venv"
ENV PATH="$VIRTUAL_ENV/bin:${PATH}"

# Default port (Cloud Run will override with PORT=8080)
ENV PORT=8000

# Use exec form with sh -c to expand PORT variable and use absolute path to uvicorn
CMD ["/bin/sh", "-c", "/app/.venv/bin/uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]
