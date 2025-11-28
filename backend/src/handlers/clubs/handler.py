"""Club handler for business logic."""
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import UserModel
from src.storage.data.sql.clubs.storage import ClubStorage
from src.storage.data.sql.user.clubs.storage import UserClubStorage
from src.storage.data.sql.users.storage import UserStorage
from src.transports.json.club_schemas import (
    AddUserToClub,
    ClubCreate,
    ClubResponse,
    ClubUpdate,
    UserClubResponse,
)


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
        self.user_club_repo = UserClubStorage(session)
        self.user_repo = UserStorage(session)

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
        # Add error handling and validation as needed

        try:

            club = await self.club_repo.create(
                name=request.name,
                description=request.description,
                topic=request.topic,
                created_by=current_user.id,
                is_active=True,
                max_members=request.max_members
            )

            # Add the creator as a member with the "owner" role
            await self.user_club_repo.add_user_to_club(
                user_id=current_user.id,
                club_id=club.id,
                role="owner"
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
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

    async def add_user_to_club(
        self,
        club_id: UUID,
        request: AddUserToClub,
        current_user: UserModel
    ) -> UserClubResponse:
        """
        Add a user to a club.

        Args:
            club_id: The club ID.
            request: Request containing user_id and role.
            current_user: The authenticated user.

        Returns:
            UserClubResponse: The created membership.

        Raises:
            HTTPException: If club not found or user not authorized.
        """
        # Check if club exists
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Club not found"
            )

        # Check if current user is authorized (must be club creator or owner)
        if club.created_by != current_user.id:
            # Check if current user is an owner
            membership = await self.user_club_repo.get_membership(
                current_user.id, club_id
            )
            if not membership or membership.role != "owner":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to add members to this club"
                )

        # Check if club has reached max capacity
        if club.max_members:
            member_count = await self.user_club_repo.get_member_count(club_id)
            if member_count >= club.max_members:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Club has reached maximum capacity"
                )

        # Check if user is already a member
        existing_membership = await self.user_club_repo.get_membership(
            request.user_id, club_id
        )
        if existing_membership:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this club"
            )

        # Add user to club
        membership = await self.user_club_repo.add_user_to_club(
            user_id=request.user_id,
            club_id=club_id,
            role=request.role
        )

        return UserClubResponse.model_validate(membership)

    async def get_user_clubs(self, user_id: UUID) -> List[ClubResponse]:
        """
        Get all clubs a user is a member of.

        Args:
            user_id: The user ID.

        Returns:
            List[ClubResponse]: List of clubs the user belongs to.
        """
        # Get all memberships for the user
        memberships = await self.user_club_repo.get_user_clubs(user_id)

        # Get club details for each membership
        clubs = []
        for membership in memberships:
            club = await self.club_repo.get_by_id(membership.club_id)
            if club:
                clubs.append(ClubResponse.model_validate(club))

        return clubs

    async def get_club_members(
        self,
        club_id: UUID
    ) -> List[UserClubResponse]:
        """
        Get all members of a club.

        Args:
            club_id: The club ID.

        Returns:
            List[UserClubResponse]: List of club memberships.

        Raises:
            HTTPException: If club not found.
        """
        # Check if club exists
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Club not found"
            )

        # Get all members
        memberships = await self.user_club_repo.get_club_members(club_id)

        # Enrich with user details
        responses = []
        for membership in memberships:
            user = await self.user_repo.get_by_id(membership.user_id)
            response_data = {
                "user_id": membership.user_id,
                "club_id": membership.club_id,
                "join_date": membership.join_date,
                "role": membership.role,
                "username": user.username if user else None,
                "full_name": user.full_name if user else None,
                "email": user.email if user else None,
            }
            responses.append(UserClubResponse(**response_data))

        return responses

    async def remove_user_from_club(
        self,
        club_id: UUID,
        user_id: UUID,
        current_user: UserModel
    ) -> bool:
        """
        Remove a user from a club (leave club).

        Args:
            club_id: The club ID.
            user_id: The user ID to remove.
            current_user: The authenticated user.

        Returns:
            bool: True if removed successfully.

        Raises:
            HTTPException: If club not found, user not a member, or not authorized.
        """
        # Check if club exists
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Club not found"
            )

        # Check if user is a member of the club
        membership = await self.user_club_repo.get_membership(user_id, club_id)
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not a member of this club"
            )

        # Authorization: Users can remove themselves, or owners can remove others
        # The club creator (owner) cannot be removed
        if membership.role == "owner" and club.created_by == user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Club owner cannot leave the club. Delete the club instead."
            )

        # Check authorization
        if user_id != current_user.id:
            # Only owners can remove other members
            current_membership = await self.user_club_repo.get_membership(
                current_user.id, club_id
            )
            if not current_membership or current_membership.role != "owner":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to remove members from this club"
                )

        # Remove user from club
        removed = await self.user_club_repo.remove_user_from_club(user_id, club_id)
        if not removed:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove user from club"
            )

        return True
