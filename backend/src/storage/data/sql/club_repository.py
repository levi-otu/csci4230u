"""Repository for club-related operations."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.club import Club, ClubMeeting
from src.storage.data.sql.base_repository import BaseRepository


class ClubRepository(BaseRepository[Club]):
    """Repository for Club model."""

    def __init__(self, session: AsyncSession):
        """Initialize club repository."""
        super().__init__(Club, session)

    async def get_by_topic(
        self,
        topic: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Club]:
        """
        Get clubs by topic.

        Args:
            topic: The topic to filter by.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Club]: List of clubs matching the topic.
        """
        stmt = (
            select(Club)
            .where(Club.topic == topic)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_active_clubs(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Club]:
        """
        Get active clubs.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Club]: List of active clubs.
        """
        stmt = (
            select(Club)
            .where(Club.is_active == True)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_with_members(self, club_id: UUID) -> Optional[Club]:
        """
        Get club with its members.

        Args:
            club_id: The club ID.

        Returns:
            Optional[Club]: Club with members if found.
        """
        stmt = (
            select(Club)
            .options(selectinload(Club.members))
            .where(Club.id == club_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class ClubMeetingRepository(BaseRepository[ClubMeeting]):
    """Repository for ClubMeeting model."""

    def __init__(self, session: AsyncSession):
        """Initialize club meeting repository."""
        super().__init__(ClubMeeting, session)

    async def get_by_club_id(
        self,
        club_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[ClubMeeting]:
        """
        Get club meetings by club ID.

        Args:
            club_id: The club ID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[ClubMeeting]: List of club meetings.
        """
        stmt = (
            select(ClubMeeting)
            .where(ClubMeeting.club_id == club_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
