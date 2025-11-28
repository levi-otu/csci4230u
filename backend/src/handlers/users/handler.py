"""User handler for business logic."""
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import UserModel
from src.storage.data.sql.users.storage import UserStorage, UserSecurityStorage
from src.transports.json.user_schemas import UserResponse, UserUpdate


class UserHandler:
    """Handler for user operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize user handler.

        Args:
            session: Database session.
        """
        self.session = session
        self.user_repo = UserStorage(session)
        self.security_repo = UserSecurityStorage(session)

    async def get_user(self, user_id: UUID) -> UserResponse:
        """
        Get a user by ID.

        Args:
            user_id: The user ID.

        Returns:
            UserResponse: The user data.

        Raises:
            HTTPException: If user not found.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserResponse.model_validate(user)

    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserResponse]:
        """
        Get all users with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[UserResponse]: List of users.
        """
        users = await self.user_repo.get_all(skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]

    async def update_user(
        self,
        user_id: UUID,
        request: UserUpdate,
        current_user: UserModel
    ) -> UserResponse:
        """
        Update a user.

        Business rules:
        - Users can only update their own profile
        - Username must be unique if changed
        - Email must be unique if changed

        Args:
            user_id: The user ID to update.
            request: User update request.
            current_user: The authenticated user.

        Returns:
            UserResponse: The updated user.

        Raises:
            HTTPException: If user not found, not authorized, or validation fails.
        """
        # Check if user exists
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Business rule: Users can only update their own profile
        if user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this user"
            )

        # Validate username uniqueness if changing
        if request.username and request.username != user.username:
            existing_user = await self.user_repo.get_by_username(request.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )

        # Validate email uniqueness if changing
        if request.email and request.email != user.email:
            existing_email = await self.user_repo.get_by_email(request.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )

            # Update email in security table as well
            user_security = await self.security_repo.get_by_user_id(user_id)
            if user_security:
                # Update the security email
                security_orm = await self.session.get(
                    type(user_security).__class__,
                    user_security.user_id
                )
                if security_orm:
                    security_orm.email = request.email
                    await self.session.flush()

        # Update user
        update_data = request.model_dump(exclude_unset=True)
        updated_user = await self.user_repo.update(user_id, **update_data)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )

        return UserResponse.model_validate(updated_user)

    async def delete_user(
        self,
        user_id: UUID,
        current_user: UserModel
    ) -> bool:
        """
        Delete a user.

        Business rules:
        - Users can only delete their own account
        - Deletion is a soft delete (marks as inactive) to maintain data integrity

        Args:
            user_id: The user ID to delete.
            current_user: The authenticated user.

        Returns:
            bool: True if deleted successfully.

        Raises:
            HTTPException: If user not found or not authorized.
        """
        # Check if user exists
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Business rule: Users can only delete their own account
        if user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this user"
            )

        # Soft delete: mark as inactive instead of hard delete
        await self.user_repo.update(user_id, is_active=False)
        return True

    async def get_current_user_profile(
        self,
        current_user: UserModel
    ) -> UserResponse:
        """
        Get the current user's profile.

        Args:
            current_user: The authenticated user.

        Returns:
            UserResponse: The user's profile data.
        """
        return UserResponse.model_validate(current_user)
