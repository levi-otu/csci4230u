"""Storage for club-related operations."""
from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.club import ClubModel, ClubORM, ClubMeetingModel, ClubMeetingORM


class ClubStorage:
    """Storage for Club model - converts between ORM and domain models."""

    def __init__(self, session: AsyncSession):
        """Initialize club repository."""
        self.session = session

    def _to_domain(self, orm: Optional[ClubORM]) -> Optional[ClubModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return ClubModel.model_validate(orm)

    def _to_orm(self, domain: ClubModel) -> ClubORM:
        """Convert domain model to ORM model."""
        return ClubORM(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            topic=domain.topic,
            created_by=domain.created_by,
            is_active=domain.is_active,
            max_members=domain.max_members,
        )

    async def create(self, **kwargs: Any) -> ClubModel:
        """
        Create a new club.

        Args:
            **kwargs: Club fields.

        Returns:
            ClubModel: The created club domain model.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            orm_club = ClubORM(**kwargs)
            self.session.add(orm_club)
            await self.session.flush()
            await self.session.refresh(orm_club)
            result = self._to_domain(orm_club)
            if result is None:
                raise ValueError("Failed to create club model")
            return result
        except SQLAlchemyError as _e:
            # logger.error(f"Error creating club: {e}")
            raise

    async def get_by_id(self, club_id: UUID) -> Optional[ClubModel]:
        """
        Get club by ID.

        Args:
            club_id: The club ID.

        Returns:
            Optional[ClubModel]: The club domain model if found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(ClubORM).where(ClubORM.id == club_id)
            result = await self.session.execute(stmt)
            orm_club = result.scalar_one_or_none()
            return self._to_domain(orm_club)
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting club by id {club_id}: {e}")
            raise

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ClubModel]:
        """
        Get all clubs with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[ClubModel]: List of club domain models.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = select(ClubORM).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            orm_clubs = result.scalars().all()
            return [
                domain for orm in orm_clubs
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting all clubs: {e}")
            raise

    async def update(
        self,
        club_id: UUID,
        **kwargs: Any
    ) -> Optional[ClubModel]:
        """
        Update a club.

        Args:
            club_id: The club ID.
            **kwargs: Fields to update.

        Returns:
            Optional[ClubModel]: The updated club domain model if found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            orm_club = await self.session.get(ClubORM, club_id)
            if orm_club:
                for key, value in kwargs.items():
                    if hasattr(orm_club, key):
                        setattr(orm_club, key, value)
                await self.session.flush()
                await self.session.refresh(orm_club)
            return self._to_domain(orm_club)
        except SQLAlchemyError as _e:
            # logger.error(f"Error updating club {club_id}: {e}")
            raise

    async def delete(self, club_id: UUID) -> bool:
        """
        Delete a club.

        Args:
            club_id: The club ID.

        Returns:
            bool: True if deleted, False if not found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            orm_club = await self.session.get(ClubORM, club_id)
            if orm_club:
                await self.session.delete(orm_club)
                await self.session.flush()
                return True
            return False
        except SQLAlchemyError as _e:
            # logger.error(f"Error deleting club {club_id}: {e}")
            raise

    async def get_by_topic(
        self,
        topic: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ClubModel]:
        """
        Get clubs by topic.

        Args:
            topic: The topic to filter by.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[ClubModel]: List of clubs matching the topic.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = (
                select(ClubORM)
                .where(ClubORM.topic == topic)
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            orm_clubs = result.scalars().all()
            return [
                domain for orm in orm_clubs
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting clubs by topic {topic}: {e}")
            raise

    async def get_active_clubs(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ClubModel]:
        """
        Get active clubs.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[ClubModel]: List of active clubs.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = (
                select(ClubORM)
                .where(ClubORM.is_active == True)  # noqa: E712
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            orm_clubs = result.scalars().all()
            return [
                domain for orm in orm_clubs
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting active clubs: {e}")
            raise

    async def get_with_members(self, club_id: UUID) -> Optional[ClubModel]:
        """
        Get club with its members eagerly loaded.

        Args:
            club_id: The club ID.

        Returns:
            Optional[ClubModel]: Club with members if found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = (
                select(ClubORM)
                .options(selectinload(ClubORM.members))
                .where(ClubORM.id == club_id)
            )
            result = await self.session.execute(stmt)
            orm_club = result.scalar_one_or_none()
            return self._to_domain(orm_club)
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting club with members {club_id}: {e}")
            raise


class ClubMeetingStorage:
    """Storage for ClubMeeting model - converts between ORM and domain models."""

    def __init__(self, session: AsyncSession):
        """Initialize club meeting repository."""
        self.session = session

    def _to_domain(self, orm: Optional[ClubMeetingORM]) -> Optional[ClubMeetingModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return ClubMeetingModel.model_validate(orm)

    def _to_orm(self, domain: ClubMeetingModel) -> ClubMeetingORM:
        """Convert domain model to ORM model."""
        return ClubMeetingORM(
            id=domain.id,
            club_id=domain.club_id,
            meeting_id=domain.meeting_id,
            start_date=domain.start_date,
            end_date=domain.end_date,
            frequency=domain.frequency,
            recurrence_rule=domain.recurrence_rule,
        )

    async def create(self, **kwargs: Any) -> ClubMeetingModel:
        """
        Create a new club meeting.

        Args:
            **kwargs: Club meeting fields.

        Returns:
            ClubMeetingModel: The created club meeting domain model.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            orm_meeting = ClubMeetingORM(**kwargs)
            self.session.add(orm_meeting)
            await self.session.flush()
            await self.session.refresh(orm_meeting)
            result = self._to_domain(orm_meeting)
            if result is None:
                raise ValueError("Failed to create club meeting model")
            return result
        except SQLAlchemyError as _e:
            # logger.error(f"Error creating club meeting: {e}")
            raise

    async def get_by_club_id(
        self,
        club_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[ClubMeetingModel]:
        """
        Get club meetings by club ID.

        Args:
            club_id: The club ID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[ClubMeetingModel]: List of club meetings.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            stmt = (
                select(ClubMeetingORM)
                .where(ClubMeetingORM.club_id == club_id)
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            orm_meetings = result.scalars().all()
            return [
                domain for orm in orm_meetings
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError as _e:
            # logger.error(f"Error getting club meetings for club {club_id}: {e}")
            raise
