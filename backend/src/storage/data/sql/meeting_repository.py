"""Repository for meeting-related operations."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.meeting import Meeting
from src.storage.data.sql.base_repository import BaseRepository


class MeetingRepository(BaseRepository[Meeting]):
    """Repository for Meeting model."""

    def __init__(self, session: AsyncSession):
        """Initialize meeting repository."""
        super().__init__(Meeting, session)

    async def get_by_status(
        self,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Meeting]:
        """
        Get meetings by status.

        Args:
            status: The status to filter by.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Meeting]: List of meetings with the given status.
        """
        stmt = (
            select(Meeting)
            .where(Meeting.status == status)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_club_id(
        self,
        club_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Meeting]:
        """
        Get meetings by club ID.

        Args:
            club_id: The club ID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Meeting]: List of meetings for the club.
        """
        stmt = (
            select(Meeting)
            .where(Meeting.club_id == club_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_creator_id(
        self,
        creator_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Meeting]:
        """
        Get meetings by creator ID.

        Args:
            creator_id: The creator user ID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Meeting]: List of meetings created by the user.
        """
        stmt = (
            select(Meeting)
            .where(Meeting.created_by == creator_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
