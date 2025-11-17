"""Repository for user-related operations."""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User, UserSecurity
from src.storage.data.sql.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository."""
        super().__init__(User, session)

    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: The username to search for.

        Returns:
            Optional[User]: The user if found, None otherwise.
        """
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email: The email to search for.

        Returns:
            Optional[User]: The user if found, None otherwise.
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_security(self, user_id: str) -> Optional[User]:
        """
        Get user with security information.

        Args:
            user_id: The user ID.

        Returns:
            Optional[User]: User with security info if found.
        """
        stmt = (
            select(User)
            .options(selectinload(User.security))
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class UserSecurityRepository(BaseRepository[UserSecurity]):
    """Repository for UserSecurity model."""

    def __init__(self, session: AsyncSession):
        """Initialize user security repository."""
        super().__init__(UserSecurity, session)

    async def get_by_email(self, email: str) -> Optional[UserSecurity]:
        """
        Get user security by email.

        Args:
            email: The email to search for.

        Returns:
            Optional[UserSecurity]: The security record if found.
        """
        stmt = select(UserSecurity).where(UserSecurity.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: str) -> Optional[UserSecurity]:
        """
        Get user security by user ID.

        Args:
            user_id: The user ID.

        Returns:
            Optional[UserSecurity]: The security record if found.
        """
        stmt = select(UserSecurity).where(UserSecurity.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
