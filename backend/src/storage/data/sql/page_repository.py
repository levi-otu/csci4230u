"""Repository for page-related operations."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.page import Page
from src.storage.data.sql.base_repository import BaseRepository


class PageRepository(BaseRepository[Page]):
    """Repository for Page model."""

    def __init__(self, session: AsyncSession):
        """Initialize page repository."""
        super().__init__(Page, session)

    async def get_by_name(self, name: str) -> Optional[Page]:
        """
        Get page by name.

        Args:
            name: The page name.

        Returns:
            Optional[Page]: The page if found, None otherwise.
        """
        stmt = select(Page).where(Page.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_topic(
        self,
        topic: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Page]:
        """
        Get pages by topic.

        Args:
            topic: The topic to filter by.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Page]: List of pages matching the topic.
        """
        stmt = (
            select(Page)
            .where(Page.topic == topic)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_active_pages(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Page]:
        """
        Get active pages.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Page]: List of active pages.
        """
        stmt = (
            select(Page)
            .where(Page.is_active == True)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_with_followers(self, page_id: UUID) -> Optional[Page]:
        """
        Get page with its followers.

        Args:
            page_id: The page ID.

        Returns:
            Optional[Page]: Page with followers if found.
        """
        stmt = (
            select(Page)
            .options(selectinload(Page.followers))
            .where(Page.id == page_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
