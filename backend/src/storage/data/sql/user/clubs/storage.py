"""Storage layer for user-club associations."""
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.club import UserClubModel, user_clubs
from src.models.base import utc_now


class UserClubStorage:
    """Storage for user clubs - manages user-club memberships."""

    def __init__(self, session: AsyncSession):
        """Initialize user club repository."""
        self.session = session

    def _to_domain(self, row: Any) -> Optional[UserClubModel]:
        """Convert database row to domain model."""
        if row is None:
            return None
        return UserClubModel(
            user_id=row.user_id,
            club_id=row.club_id,
            join_date=row.join_date,
            role=row.role,
        )

    async def add_user_to_club(
        self,
        user_id: UUID,
        club_id: UUID,
        role: str = "member"
    ) -> UserClubModel:
        """
        Add a user to a club.

        Args:
            user_id: The user's ID.
            club_id: The club's ID.
            role: The user's role in the club (default: "member").

        Returns:
            UserClubModel: The created membership domain model.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = user_clubs.insert().values(
                user_id=user_id,
                club_id=club_id,
                join_date=utc_now(),
                role=role,
            )
            await self.session.execute(stmt)
            await self.session.flush()

            # Retrieve the created record
            membership = await self.get_membership(user_id, club_id)
            if membership is None:
                raise ValueError("Failed to create user club membership")
            return membership
        except SQLAlchemyError:
            raise

    async def remove_user_from_club(
        self,
        user_id: UUID,
        club_id: UUID
    ) -> bool:
        """
        Remove a user from a club.

        Args:
            user_id: The user's ID.
            club_id: The club's ID.

        Returns:
            bool: True if the membership was removed, False otherwise.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = delete(user_clubs).where(
                user_clubs.c.user_id == user_id,
                user_clubs.c.club_id == club_id,
            )
            result = await self.session.execute(stmt)
            await self.session.flush()
            return result.rowcount > 0
        except SQLAlchemyError:
            raise

    async def get_membership(
        self,
        user_id: UUID,
        club_id: UUID
    ) -> Optional[UserClubModel]:
        """
        Get a specific user-club membership.

        Args:
            user_id: The user's ID.
            club_id: The club's ID.

        Returns:
            Optional[UserClubModel]: The membership if found, None otherwise.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(user_clubs).where(
                user_clubs.c.user_id == user_id,
                user_clubs.c.club_id == club_id,
            )
            result = await self.session.execute(stmt)
            row = result.first()
            return self._to_domain(row)
        except SQLAlchemyError:
            raise

    async def get_user_clubs(self, user_id: UUID) -> list[UserClubModel]:
        """
        Get all clubs a user is a member of.

        Args:
            user_id: The user's ID.

        Returns:
            list[UserClubModel]: List of user's club memberships.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(user_clubs).where(user_clubs.c.user_id == user_id)
            result = await self.session.execute(stmt)
            rows = result.fetchall()
            memberships = []
            for row in rows:
                membership = self._to_domain(row)
                if membership:
                    memberships.append(membership)
            return memberships
        except SQLAlchemyError:
            raise

    async def get_club_members(self, club_id: UUID) -> list[UserClubModel]:
        """
        Get all members of a club.

        Args:
            club_id: The club's ID.

        Returns:
            list[UserClubModel]: List of club memberships.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(user_clubs).where(user_clubs.c.club_id == club_id)
            result = await self.session.execute(stmt)
            rows = result.fetchall()
            memberships = []
            for row in rows:
                membership = self._to_domain(row)
                if membership:
                    memberships.append(membership)
            return memberships
        except SQLAlchemyError:
            raise

    async def update_role(
        self,
        user_id: UUID,
        club_id: UUID,
        new_role: str
    ) -> Optional[UserClubModel]:
        """
        Update a user's role in a club.

        Args:
            user_id: The user's ID.
            club_id: The club's ID.
            new_role: The new role for the user.

        Returns:
            Optional[UserClubModel]: The updated membership if found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = (
                update(user_clubs)
                .where(
                    user_clubs.c.user_id == user_id,
                    user_clubs.c.club_id == club_id,
                )
                .values(role=new_role)
            )
            result = await self.session.execute(stmt)
            await self.session.flush()

            if result.rowcount == 0:
                return None

            # Retrieve the updated record
            return await self.get_membership(user_id, club_id)
        except SQLAlchemyError:
            raise

    async def is_member(self, user_id: UUID, club_id: UUID) -> bool:
        """
        Check if a user is a member of a club.

        Args:
            user_id: The user's ID.
            club_id: The club's ID.

        Returns:
            bool: True if the user is a member, False otherwise.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        membership = await self.get_membership(user_id, club_id)
        return membership is not None

    async def get_member_count(self, club_id: UUID) -> int:
        """
        Get the number of members in a club.

        Args:
            club_id: The club's ID.

        Returns:
            int: The number of members.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(user_clubs).where(user_clubs.c.club_id == club_id)
            result = await self.session.execute(stmt)
            rows = result.fetchall()
            return len(rows)
        except SQLAlchemyError:
            raise
