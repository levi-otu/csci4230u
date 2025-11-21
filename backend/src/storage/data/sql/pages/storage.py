"""Storage for page-related operations."""
from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.page import PageModel, PageORM


class PageStorage:
    """Storage for Page model - converts between ORM and domain models."""

    def __init__(self, session: AsyncSession):
        """Initialize page repository."""
        self.session = session

    def _to_domain(self, orm: Optional[PageORM]) -> Optional[PageModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return PageModel.model_validate(orm)

    async def create(self, **kwargs: Any) -> PageModel:
        """Create a new page."""
        try:
            orm_page = PageORM(**kwargs)
            self.session.add(orm_page)
            await self.session.flush()
            await self.session.refresh(orm_page)
            result = self._to_domain(orm_page)
            if result is None:
                raise ValueError("Failed to create page model")
            return result
        except SQLAlchemyError:
            raise

    async def get_by_id(self, page_id: UUID) -> Optional[PageModel]:
        """Get page by ID."""
        try:
            stmt = select(PageORM).where(PageORM.id == page_id)
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[PageModel]:
        """Get all pages."""
        try:
            stmt = select(PageORM).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise

    async def update(self, page_id: UUID, **kwargs: Any) -> Optional[PageModel]:
        """Update a page."""
        try:
            orm_page = await self.session.get(PageORM, page_id)
            if orm_page:
                for key, value in kwargs.items():
                    if hasattr(orm_page, key):
                        setattr(orm_page, key, value)
                await self.session.flush()
                await self.session.refresh(orm_page)
            return self._to_domain(orm_page)
        except SQLAlchemyError:
            raise

    async def delete(self, page_id: UUID) -> bool:
        """Delete a page."""
        try:
            orm_page = await self.session.get(PageORM, page_id)
            if orm_page:
                await self.session.delete(orm_page)
                await self.session.flush()
                return True
            return False
        except SQLAlchemyError:
            raise

    async def get_by_name(self, name: str) -> Optional[PageModel]:
        """Get page by name."""
        try:
            stmt = select(PageORM).where(PageORM.name == name)
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def get_by_topic(
        self, topic: str, skip: int = 0, limit: int = 100
    ) -> List[PageModel]:
        """Get pages by topic."""
        try:
            stmt = (
                select(PageORM)
                .where(PageORM.topic == topic)
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

    async def get_active_pages(
        self, skip: int = 0, limit: int = 100
    ) -> List[PageModel]:
        """Get active pages."""
        try:
            stmt = (
                select(PageORM)
                .where(PageORM.is_active == True)  # noqa: E712
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

    async def get_with_followers(self, page_id: UUID) -> Optional[PageModel]:
        """Get page with its followers eagerly loaded."""
        try:
            stmt = (
                select(PageORM)
                .options(selectinload(PageORM.followers))
                .where(PageORM.id == page_id)
            )
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise
