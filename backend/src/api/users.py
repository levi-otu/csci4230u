"""User API endpoints."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_active_user
from src.database import get_db
from src.handlers.users.handler import UserHandler
from src.models.user import UserModel
from src.transports.json.user_schemas import UserResponse, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: UserModel = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Get the current authenticated user's profile.

    Args:
        current_user: The authenticated user.
        session: Database session.

    Returns:
        UserResponse: The current user's profile.
    """
    handler = UserHandler(session)
    return await handler.get_current_user_profile(current_user)


@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> List[UserResponse]:
    """
    Get all users with pagination.
    Requires authentication.

    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        session: Database session.
        current_user: Authenticated user.

    Returns:
        List[UserResponse]: List of users.
    """
    handler = UserHandler(session)
    return await handler.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserResponse:
    """
    Get a user by ID.
    Requires authentication.

    Args:
        user_id: The user ID.
        session: Database session.
        current_user: Authenticated user.

    Returns:
        UserResponse: The user data.
    """
    handler = UserHandler(session)
    return await handler.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    request: UserUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> UserResponse:
    """
    Update a user.

    Business rules enforced:
    - Users can only update their own profile
    - Username must be unique if changed
    - Email must be unique if changed

    Args:
        user_id: The user ID.
        request: User update data.
        session: Database session.
        current_user: Authenticated user.

    Returns:
        UserResponse: The updated user.
    """
    handler = UserHandler(session)
    return await handler.update_user(user_id, request, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
) -> None:
    """
    Delete a user (soft delete - marks as inactive).

    Business rules enforced:
    - Users can only delete their own account
    - Deletion is a soft delete to maintain data integrity

    Args:
        user_id: The user ID.
        session: Database session.
        current_user: Authenticated user.
    """
    handler = UserHandler(session)
    await handler.delete_user(user_id, current_user)
