"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_active_user
from src.config import settings
from src.database import get_db
from src.handlers.users.auth.handler import AuthHandler
from src.models.user import UserModel
from src.transports.json.auth_schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    request: RegisterRequest,
    response: Response,
    user_agent: str | None = Header(None),
    x_forwarded_for: str | None = Header(None),
    session: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Register a new user.

    Args:
        request: Registration data (username, email, password).
        response: HTTP response for setting cookies.
        user_agent: User agent string from header.
        x_forwarded_for: Client IP from proxy header.
        session: Database session.

    Returns:
        TokenResponse: JWT access token (refresh token in httpOnly cookie).
    """
    handler = AuthHandler(session)
    tokens = await handler.register(
        request,
        device_info=user_agent,
        ip_address=x_forwarded_for
    )

    # Set httpOnly cookie for refresh token
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        domain=settings.COOKIE_DOMAIN,
        path="/"
    )

    # Return only access token in response body
    return TokenResponse(
        access_token=tokens.access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    response: Response,
    user_agent: str | None = Header(None),
    x_forwarded_for: str | None = Header(None),
    session: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Login a user.

    Args:
        request: Login credentials (email, password).
        response: HTTP response for setting cookies.
        user_agent: User agent string from header.
        x_forwarded_for: Client IP from proxy header.
        session: Database session.

    Returns:
        TokenResponse: JWT access token (refresh token in httpOnly cookie).
    """
    handler = AuthHandler(session)
    tokens = await handler.login(
        request,
        device_info=user_agent,
        ip_address=x_forwarded_for
    )

    # Set httpOnly cookie for refresh token
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        domain=settings.COOKIE_DOMAIN,
        path="/"
    )

    # Return only access token in response body
    return TokenResponse(
        access_token=tokens.access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Request,
    session: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Refresh access token using httpOnly cookie.

    Args:
        request: HTTP request containing refresh token cookie.
        session: Database session.

    Returns:
        TokenResponse: New JWT access token.

    Raises:
        HTTPException: If no refresh token or token is invalid.
    """
    refresh_token_value = request.cookies.get("refresh_token")
    if not refresh_token_value:
        raise HTTPException(
            status_code=401,
            detail="No refresh token provided"
        )

    handler = AuthHandler(session)
    return await handler.refresh_access_token(refresh_token_value)


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    current_user: UserModel = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db)
) -> dict:
    """
    Logout and revoke refresh token.

    Args:
        request: HTTP request containing refresh token cookie.
        response: HTTP response for clearing cookies.
        current_user: The authenticated user.
        session: Database session.

    Returns:
        dict: Success message.
    """
    refresh_token_value = request.cookies.get("refresh_token")

    handler = AuthHandler(session)
    await handler.logout(current_user.id, refresh_token_value)

    # Clear cookie
    response.delete_cookie(key="refresh_token", path="/")

    return {"message": "Logged out successfully"}


@router.post("/logout-all")
async def logout_all_devices(
    response: Response,
    current_user: UserModel = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db)
) -> dict:
    """
    Logout from all devices.

    Args:
        response: HTTP response for clearing cookies.
        current_user: The authenticated user.
        session: Database session.

    Returns:
        dict: Success message with count.
    """
    handler = AuthHandler(session)
    count = await handler.logout_all_devices(current_user.id)

    # Clear cookie
    response.delete_cookie(key="refresh_token", path="/")

    return {"message": f"Logged out from {count} device(s)"}
