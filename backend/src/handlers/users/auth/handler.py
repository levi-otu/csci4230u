"""Authentication handler for user registration and login."""
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import UserModel, UserSecurityModel
from src.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from src.storage.data.sql.users.storage import (
    UserStorage,
    UserSecurityStorage,
)
from src.storage.data.sql.refresh_tokens.storage import RefreshTokenStorage
from src.transports.json.auth_schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)


import uuid

class AuthHandler:
    """Handler for authentication operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize auth handler.

        Args:
            session: Database session.
        """
        self.session = session
        self.user_repo = UserStorage(session)
        self.security_repo = UserSecurityStorage(session)
        self.refresh_token_repo = RefreshTokenStorage(session)

    async def register(
        self,
        request: RegisterRequest,
        device_info: str | None = None,
        ip_address: str | None = None
    ) -> TokenResponse:
        """
        Register a new user.

        Args:
            request: Registration request data.
            device_info: Optional device/user-agent information.
            ip_address: Optional IP address.

        Returns:
            TokenResponse: JWT tokens.

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
            # generate uuid for id
            id=uuid.uuid4(),
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
            password_changed_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )

        # Generate tokens
        access_token = create_access_token(subject=str(user.id))
        refresh_token, expires_at = create_refresh_token(subject=str(user.id))

        # Store refresh token in database
        await self.refresh_token_repo.create_token(
            user_id=user.id,
            token=refresh_token,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def login(
        self,
        request: LoginRequest,
        device_info: str | None = None,
        ip_address: str | None = None
    ) -> TokenResponse:
        """
        Login a user.

        Args:
            request: Login request data.
            device_info: Optional device/user-agent information.
            ip_address: Optional IP address.

        Returns:
            TokenResponse: JWT tokens.

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

        # Generate tokens
        access_token = create_access_token(subject=str(user.id))
        refresh_token, expires_at = create_refresh_token(subject=str(user.id))

        # Store refresh token in database
        await self.refresh_token_repo.create_token(
            user_id=user.id,
            token=refresh_token,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """
        Exchange refresh token for new access token.

        Args:
            refresh_token: The refresh token from httpOnly cookie.

        Returns:
            TokenResponse: New access token.

        Raises:
            HTTPException: If refresh token is invalid or expired.
        """
        # Verify refresh token JWT
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # Check if token exists and is valid in database
        token_record = await self.refresh_token_repo.get_by_token(refresh_token)
        if not token_record or not token_record.is_valid():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token revoked or expired"
            )

        # Generate new access token
        user_id = payload.get("sub")
        access_token = create_access_token(subject=user_id)

        return TokenResponse(access_token=access_token)

    async def logout(self, user_id: UUID, refresh_token: str | None = None) -> bool:
        """
        Logout user and revoke refresh token.

        Args:
            user_id: The user ID.
            refresh_token: Optional refresh token to revoke.

        Returns:
            bool: True if successful.
        """
        if refresh_token:
            token_record = await self.refresh_token_repo.get_by_token(refresh_token)
            if token_record:
                await self.refresh_token_repo.revoke_token(token_record.id)
        return True

    async def logout_all_devices(self, user_id: UUID) -> int:
        """
        Logout user from all devices.

        Args:
            user_id: The user ID.

        Returns:
            int: Number of tokens revoked.
        """
        count = await self.refresh_token_repo.revoke_all_user_tokens(user_id)
        return count
