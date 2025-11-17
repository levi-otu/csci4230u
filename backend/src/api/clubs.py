"""Club API endpoints."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_active_user
from src.database import get_db
from src.handlers.clubs.club_handler import ClubHandler
from src.models.user import User
from src.transports.json.club_schemas import ClubCreate, ClubResponse, ClubUpdate

router = APIRouter(prefix="/api/clubs", tags=["clubs"])


@router.post("", response_model=ClubResponse, status_code=status.HTTP_201_CREATED)
async def create_club(
    request: ClubCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ClubResponse:
    """
    Create a new club.

    Args:
        request: Club creation data.
        session: Database session.
        current_user: Authenticated user.

    Returns:
        ClubResponse: The created club.
    """
    handler = ClubHandler(session)
    return await handler.create_club(request, current_user)


@router.get("", response_model=List[ClubResponse])
async def get_clubs(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
) -> List[ClubResponse]:
    """
    Get all clubs.

    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        session: Database session.

    Returns:
        List[ClubResponse]: List of clubs.
    """
    handler = ClubHandler(session)
    return await handler.get_clubs(skip=skip, limit=limit)


@router.get("/{club_id}", response_model=ClubResponse)
async def get_club(
    club_id: UUID,
    session: AsyncSession = Depends(get_db)
) -> ClubResponse:
    """
    Get a club by ID.

    Args:
        club_id: The club ID.
        session: Database session.

    Returns:
        ClubResponse: The club data.
    """
    handler = ClubHandler(session)
    return await handler.get_club(club_id)


@router.put("/{club_id}", response_model=ClubResponse)
async def update_club(
    club_id: UUID,
    request: ClubUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ClubResponse:
    """
    Update a club.

    Args:
        club_id: The club ID.
        request: Club update data.
        session: Database session.
        current_user: Authenticated user.

    Returns:
        ClubResponse: The updated club.
    """
    handler = ClubHandler(session)
    return await handler.update_club(club_id, request, current_user)


@router.delete("/{club_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_club(
    club_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete a club.

    Args:
        club_id: The club ID.
        session: Database session.
        current_user: Authenticated user.
    """
    handler = ClubHandler(session)
    await handler.delete_club(club_id, current_user)
