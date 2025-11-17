"""Repository for book-related operations."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.book import Book, BookVersion, Publisher
from src.storage.data.sql.base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    """Repository for Book model."""

    def __init__(self, session: AsyncSession):
        """Initialize book repository."""
        super().__init__(Book, session)

    async def search_by_title(
        self,
        title: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Book]:
        """
        Search books by title.

        Args:
            title: The title to search for (case-insensitive).
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Book]: List of books matching the title.
        """
        stmt = (
            select(Book)
            .where(Book.title.ilike(f"%{title}%"))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_author(
        self,
        author: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Book]:
        """
        Get books by author.

        Args:
            author: The author name.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Book]: List of books by the author.
        """
        stmt = (
            select(Book)
            .where(Book.author.ilike(f"%{author}%"))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_genre(
        self,
        genre: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Book]:
        """
        Get books by genre.

        Args:
            genre: The genre to filter by.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[Book]: List of books in the genre.
        """
        stmt = (
            select(Book)
            .where(Book.genre == genre)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_with_versions(self, book_id: UUID) -> Optional[Book]:
        """
        Get book with all its versions.

        Args:
            book_id: The book ID.

        Returns:
            Optional[Book]: Book with versions if found.
        """
        stmt = (
            select(Book)
            .options(selectinload(Book.versions))
            .where(Book.id == book_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class BookVersionRepository(BaseRepository[BookVersion]):
    """Repository for BookVersion model."""

    def __init__(self, session: AsyncSession):
        """Initialize book version repository."""
        super().__init__(BookVersion, session)

    async def get_by_isbn(self, isbn: str) -> Optional[BookVersion]:
        """
        Get book version by ISBN.

        Args:
            isbn: The ISBN to search for.

        Returns:
            Optional[BookVersion]: The book version if found.
        """
        stmt = select(BookVersion).where(BookVersion.isbn == isbn)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_book_id(
        self,
        book_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[BookVersion]:
        """
        Get versions by book ID.

        Args:
            book_id: The book ID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List[BookVersion]: List of book versions.
        """
        stmt = (
            select(BookVersion)
            .where(BookVersion.book_id == book_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class PublisherRepository(BaseRepository[Publisher]):
    """Repository for Publisher model."""

    def __init__(self, session: AsyncSession):
        """Initialize publisher repository."""
        super().__init__(Publisher, session)

    async def get_by_name(self, name: str) -> Optional[Publisher]:
        """
        Get publisher by name.

        Args:
            name: The publisher name.

        Returns:
            Optional[Publisher]: The publisher if found.
        """
        stmt = select(Publisher).where(Publisher.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
