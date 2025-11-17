"""Authentication API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.handlers.users.auth_handler import AuthHandler
from src.transports.json.auth_schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    request: RegisterRequest,
    session: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Register a new user.

    Args:
        request: Registration data (username, email, password).
        session: Database session.

    Returns:
        TokenResponse: JWT access token.
    """
    handler = AuthHandler(session)
    return await handler.register(request)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Login a user.

    Args:
        request: Login credentials (email, password).
        session: Database session.

    Returns:
        TokenResponse: JWT access token.
    """
    handler = AuthHandler(session)
    return await handler.login(request)
