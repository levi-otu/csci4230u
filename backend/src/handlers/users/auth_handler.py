"""Authentication handler for user registration and login."""
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User, UserSecurity
from src.security import create_access_token, get_password_hash, verify_password
from src.storage.data.sql.user_repository import (
    UserRepository,
    UserSecurityRepository,
)
from src.transports.json.auth_schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)


class AuthHandler:
    """Handler for authentication operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize auth handler.

        Args:
            session: Database session.
        """
        self.session = session
        self.user_repo = UserRepository(session)
        self.security_repo = UserSecurityRepository(session)

    async def register(self, request: RegisterRequest) -> TokenResponse:
        """
        Register a new user.

        Args:
            request: Registration request data.

        Returns:
            TokenResponse: JWT access token.

        Raises:
            HTTPException: If username or email already exists.
        """
        # Check if username exists
        existing_user = await self.user_repo.get_by_username(request.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if email exists
        existing_email = await self.user_repo.get_by_email(request.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create user
        user = await self.user_repo.create(
            username=request.username,
            email=request.email,
            full_name=request.full_name,
            is_active=True
        )

        # Create user security
        hashed_password = get_password_hash(request.password)
        await self.security_repo.create(
            user_id=user.id,
            email=request.email,
            password=hashed_password,
            password_changed_at=datetime.utcnow()
        )

        # Generate token
        access_token = create_access_token(subject=str(user.id))

        return TokenResponse(access_token=access_token)

    async def login(self, request: LoginRequest) -> TokenResponse:
        """
        Login a user.

        Args:
            request: Login request data.

        Returns:
            TokenResponse: JWT access token.

        Raises:
            HTTPException: If credentials are invalid.
        """
        # Get user security by email
        user_security = await self.security_repo.get_by_email(request.email)
        if not user_security:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Verify password
        if not verify_password(request.password, user_security.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Get user
        user = await self.user_repo.get_by_id(user_security.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        # Generate token
        access_token = create_access_token(subject=str(user.id))

        return TokenResponse(access_token=access_token)
