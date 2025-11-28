"""Storage for user-related operations."""
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import UserModel, UserORM, UserSecurityModel, UserSecurityORM


class UserStorage:
    """Storage for User model - converts between ORM and domain models."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository."""
        self.session = session

    def _to_domain(self, orm: Optional[UserORM]) -> Optional[UserModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return UserModel.model_validate(orm)

    def _to_orm(self, domain: UserModel) -> UserORM:
        """Convert domain model to ORM model."""
        return UserORM(
            id=domain.id,
            username=domain.username,
            email=domain.email,
            full_name=domain.full_name,
            is_active=domain.is_active,
        )

    async def create(self, **kwargs: Any) -> UserModel:
        """
        Create a new user.

        Args:
            **kwargs: User fields (username, email, full_name, is_active).

        Returns:
            UserModel: The created user domain model.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            orm_user = UserORM(**kwargs)
            self.session.add(orm_user)
            await self.session.flush()
            await self.session.refresh(orm_user)
            result = self._to_domain(orm_user)
            if result is None:
                raise ValueError("Failed to create user model")
            return result
        except SQLAlchemyError as _e:
            # logger.error(f"Error creating user: {e}")
            raise

    async def get_by_id(self, user_id: UUID) -> Optional[UserModel]:
        """
        Get user by ID.

        Args:
            user_id: The user ID to search for.

        Returns:
            Optional[UserModel]: The user domain model if found, None otherwise.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(UserORM).where(UserORM.id == user_id)
            result = await self.session.execute(stmt)
            orm_user = result.scalar_one_or_none()
            return self._to_domain(orm_user)
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting user by id {user_id}: {e}")
            raise

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        """
        Get user by username.

        Args:
            username: The username to search for.

        Returns:
            Optional[UserModel]: The user domain model if found, None otherwise.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(UserORM).where(UserORM.username == username)
            result = await self.session.execute(stmt)
            orm_user = result.scalar_one_or_none()
            return self._to_domain(orm_user)
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting user by username {username}: {e}")
            raise

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        """
        Get user by email.

        Args:
            email: The email to search for.

        Returns:
            Optional[UserModel]: The user domain model if found, None otherwise.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(UserORM).where(UserORM.email == email)
            result = await self.session.execute(stmt)
            orm_user = result.scalar_one_or_none()
            return self._to_domain(orm_user)
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting user by email {email}: {e}")
            raise

    async def get_with_security(self, user_id: UUID) -> Optional[UserModel]:
        """
        Get user with security information eagerly loaded.

        Args:
            user_id: The user ID.

        Returns:
            Optional[UserModel]: User domain model with security info if found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = (
                select(UserORM)
                .options(selectinload(UserORM.security))
                .where(UserORM.id == user_id)
            )
            result = await self.session.execute(stmt)
            orm_user = result.scalar_one_or_none()
            return self._to_domain(orm_user)
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting user with security for id {user_id}: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        """
        Get all users with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            list[UserModel]: List of user domain models.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(UserORM).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            orm_users = result.scalars().all()
            return [self._to_domain(user) for user in orm_users if user is not None]
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting all users: {e}")
            raise

    async def update(self, user_id: UUID, **kwargs: Any) -> Optional[UserModel]:
        """
        Update a user.

        Args:
            user_id: The user ID.
            **kwargs: Fields to update.

        Returns:
            Optional[UserModel]: The updated user domain model if found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            orm_user = await self.session.get(UserORM, user_id)
            if orm_user:
                for key, value in kwargs.items():
                    if hasattr(orm_user, key) and value is not None:
                        setattr(orm_user, key, value)
                await self.session.flush()
                await self.session.refresh(orm_user)
                return self._to_domain(orm_user)
            return None
        except SQLAlchemyError as _e:
            # logger.error(f"Error updating user {user_id}: {e}")
            raise

    async def delete(self, user_id: UUID) -> bool:
        """
        Delete a user.

        Args:
            user_id: The user ID.

        Returns:
            bool: True if deleted, False if not found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            orm_user = await self.session.get(UserORM, user_id)
            if orm_user:
                await self.session.delete(orm_user)
                await self.session.flush()
                return True
            return False
        except SQLAlchemyError as _e:
            # logger.error(f"Error deleting user {user_id}: {e}")
            raise


class UserSecurityStorage:
    """Storage for UserSecurity model - converts between ORM and domain models."""

    def __init__(self, session: AsyncSession):
        """Initialize user security repository."""
        self.session = session

    def _to_domain(self, orm: Optional[UserSecurityORM]) -> Optional[UserSecurityModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return UserSecurityModel.model_validate(orm)

    def _to_orm(self, domain: UserSecurityModel) -> UserSecurityORM:
        """Convert domain model to ORM model."""
        return UserSecurityORM(
            user_id=domain.user_id,
            email=domain.email,
            password=domain.password,
            old_password=domain.old_password,
            password_changed_at=domain.password_changed_at,
        )

    async def create(self, **kwargs: Any) -> UserSecurityModel:
        """
        Create a new user security record.

        Args:
            **kwargs: Security fields (user_id, email, password, etc.).

        Returns:
            UserSecurityModel: The created security domain model.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            orm_security = UserSecurityORM(**kwargs)
            self.session.add(orm_security)
            await self.session.flush()
            await self.session.refresh(orm_security)
            result = self._to_domain(orm_security)
            if result is None:
                raise ValueError("Failed to create user security model")
            return result
        except SQLAlchemyError as _e:
            # logger.error(f"Error creating user security: {e}")
            raise

    async def get_by_email(self, email: str) -> Optional[UserSecurityModel]:
        """
        Get user security by email.

        Args:
            email: The email to search for.

        Returns:
            Optional[UserSecurityModel]: The security domain model if found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(UserSecurityORM).where(UserSecurityORM.email == email)
            result = await self.session.execute(stmt)
            orm_security = result.scalar_one_or_none()
            return self._to_domain(orm_security)
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting user security by email {email}: {e}")
            raise

    async def get_by_user_id(self, user_id: UUID) -> Optional[UserSecurityModel]:
        """
        Get user security by user ID.

        Args:
            user_id: The user ID.

        Returns:
            Optional[UserSecurityModel]: The security domain model if found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(UserSecurityORM).where(UserSecurityORM.user_id == user_id)
            result = await self.session.execute(stmt)
            orm_security = result.scalar_one_or_none()
            return self._to_domain(orm_security)
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting user security by user_id {user_id}: {e}")
            raise
