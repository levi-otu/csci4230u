"""Club handler for business logic."""
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.club import ClubModel
from src.models.user import UserModel
from src.storage.data.sql.clubs.storage import ClubStorage
from src.transports.json.club_schemas import ClubCreate, ClubResponse, ClubUpdate


class ClubHandler:
    """Handler for club operations."""

    def __init__(self, session: AsyncSession):
        """
        Initialize club handler.

        Args:
            session: Database session.
        """
        self.session = session
        self.club_repo = ClubStorage(session)

    async def create_club(
        self,
        request: ClubCreate,
        current_user: UserModel
    ) -> ClubResponse:
        """
        Create a new club.

        Args:
            request: Club creation request.
            current_user: The authenticated user.

        Returns:
            ClubResponse: The created club.
        """
        club = await self.club_repo.create(
            name=request.name,
            description=request.description,
            topic=request.topic,
            created_by=current_user.id,
            is_active=True,
            max_members=request.max_members
        )

        return ClubResponse.model_validate(club)

    async def get_club(self, club_id: UUID) -> ClubResponse:
        """
        Get a club by ID.

        Args:
            club_id: The club ID.

        Returns:
            ClubResponse: The club data.

        Raises:
            HTTPException: If club not found.
        """
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Club not found"
            )

        return ClubResponse.model_validate(club)

    async def get_clubs(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ClubResponse]:
        """
        Get all clubs with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[ClubResponse]: List of clubs.
        """
        clubs = await self.club_repo.get_all(skip=skip, limit=limit)
        return [ClubResponse.model_validate(club) for club in clubs]

    async def update_club(
        self,
        club_id: UUID,
        request: ClubUpdate,
        current_user: UserModel
    ) -> ClubResponse:
        """
        Update a club.

        Args:
            club_id: The club ID.
            request: Club update request.
            current_user: The authenticated user.

        Returns:
            ClubResponse: The updated club.

        Raises:
            HTTPException: If club not found or user not authorized.
        """
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Club not found"
            )

        # Check if user is the creator (RBAC can be added later)
        if club.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this club"
            )

        # Update club
        update_data = request.model_dump(exclude_unset=True)
        updated_club = await self.club_repo.update(club_id, **update_data)

        return ClubResponse.model_validate(updated_club)

    async def delete_club(
        self,
        club_id: UUID,
        current_user: UserModel
    ) -> bool:
        """
        Delete a club.

        Args:
            club_id: The club ID.
            current_user: The authenticated user.

        Returns:
            bool: True if deleted successfully.

        Raises:
            HTTPException: If club not found or user not authorized.
        """
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Club not found"
            )

        # Check if user is the creator
        if club.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this club"
            )

        return await self.club_repo.delete(club_id)
