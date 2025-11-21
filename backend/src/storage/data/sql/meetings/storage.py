"""Storage for meeting-related operations."""
from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.meeting import MeetingModel, MeetingORM


class MeetingStorage:
    """Storage for Meeting model - converts between ORM and domain models."""

    def __init__(self, session: AsyncSession):
        """Initialize meeting repository."""
        self.session = session

    def _to_domain(self, orm: Optional[MeetingORM]) -> Optional[MeetingModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return MeetingModel.model_validate(orm)

    async def create(self, **kwargs: Any) -> MeetingModel:
        """Create a new meeting."""
        try:
            orm_meeting = MeetingORM(**kwargs)
            self.session.add(orm_meeting)
            await self.session.flush()
            await self.session.refresh(orm_meeting)
            result = self._to_domain(orm_meeting)
            if result is None:
                raise ValueError("Failed to create meeting model")
            return result
        except SQLAlchemyError:
            raise

    async def get_by_id(self, meeting_id: UUID) -> Optional[MeetingModel]:
        """Get meeting by ID."""
        try:
            stmt = select(MeetingORM).where(MeetingORM.id == meeting_id)
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[MeetingModel]:
        """Get all meetings."""
        try:
            stmt = select(MeetingORM).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise

    async def update(self, meeting_id: UUID, **kwargs: Any) -> Optional[MeetingModel]:
        """Update a meeting."""
        try:
            orm_meeting = await self.session.get(MeetingORM, meeting_id)
            if orm_meeting:
                for key, value in kwargs.items():
                    if hasattr(orm_meeting, key):
                        setattr(orm_meeting, key, value)
                await self.session.flush()
                await self.session.refresh(orm_meeting)
            return self._to_domain(orm_meeting)
        except SQLAlchemyError:
            raise

    async def delete(self, meeting_id: UUID) -> bool:
        """Delete a meeting."""
        try:
            orm_meeting = await self.session.get(MeetingORM, meeting_id)
            if orm_meeting:
                await self.session.delete(orm_meeting)
                await self.session.flush()
                return True
            return False
        except SQLAlchemyError:
            raise

    async def get_by_status(
        self, status: str, skip: int = 0, limit: int = 100
    ) -> List[MeetingModel]:
        """Get meetings by status."""
        try:
            stmt = (
                select(MeetingORM)
                .where(MeetingORM.status == status)
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise

    async def get_by_club_id(
        self, club_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[MeetingModel]:
        """Get meetings by club ID."""
        try:
            stmt = (
                select(MeetingORM)
                .where(MeetingORM.club_id == club_id)
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise

    async def get_by_creator_id(
        self, creator_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[MeetingModel]:
        """Get meetings by creator ID."""
        try:
            stmt = (
                select(MeetingORM)
                .where(MeetingORM.created_by == creator_id)
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise
