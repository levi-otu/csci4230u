"""Storage for book-related operations."""
from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.book import (
    BookModel,
    BookORM,
    BookVersionModel,
    BookVersionORM,
    PublisherModel,
    PublisherORM,
)


class BookStorage:
    """Storage for Book model - converts between ORM and domain models."""

    def __init__(self, session: AsyncSession):
        """Initialize book repository."""
        self.session = session

    def _to_domain(self, orm: Optional[BookORM]) -> Optional[BookModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return BookModel.model_validate(orm)

    async def create(self, **kwargs: Any) -> BookModel:
        """Create a new book."""
        try:
            orm_book = BookORM(**kwargs)
            self.session.add(orm_book)
            await self.session.flush()
            await self.session.refresh(orm_book)
            result = self._to_domain(orm_book)
            if result is None:
                raise ValueError("Failed to create book model")
            return result
        except SQLAlchemyError:
            raise

    async def get_by_id(self, book_id: UUID) -> Optional[BookModel]:
        """Get book by ID."""
        try:
            stmt = select(BookORM).where(BookORM.id == book_id)
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[BookModel]:
        """Get all books."""
        try:
            stmt = select(BookORM).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise

    async def update(self, book_id: UUID, **kwargs: Any) -> Optional[BookModel]:
        """Update a book."""
        try:
            orm_book = await self.session.get(BookORM, book_id)
            if orm_book:
                for key, value in kwargs.items():
                    if hasattr(orm_book, key):
                        setattr(orm_book, key, value)
                await self.session.flush()
                await self.session.refresh(orm_book)
            return self._to_domain(orm_book)
        except SQLAlchemyError:
            raise

    async def delete(self, book_id: UUID) -> bool:
        """Delete a book."""
        try:
            orm_book = await self.session.get(BookORM, book_id)
            if orm_book:
                await self.session.delete(orm_book)
                await self.session.flush()
                return True
            return False
        except SQLAlchemyError:
            raise

    async def search_by_title(
        self, title: str, skip: int = 0, limit: int = 100
    ) -> List[BookModel]:
        """Search books by title."""
        try:
            stmt = (
                select(BookORM)
                .where(BookORM.title.ilike(f"%{title}%"))
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

    async def get_by_author(
        self, author: str, skip: int = 0, limit: int = 100
    ) -> List[BookModel]:
        """Get books by author."""
        try:
            stmt = (
                select(BookORM)
                .where(BookORM.author.ilike(f"%{author}%"))
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

    async def get_by_genre(
        self, genre: str, skip: int = 0, limit: int = 100
    ) -> List[BookModel]:
        """Get books by genre."""
        try:
            stmt = (
                select(BookORM).where(BookORM.genre == genre).offset(skip).limit(limit)
            )
            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise

    async def get_with_versions(self, book_id: UUID) -> Optional[BookModel]:
        """Get book with all its versions."""
        try:
            stmt = (
                select(BookORM)
                .options(selectinload(BookORM.versions))
                .where(BookORM.id == book_id)
            )
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise


class BookVersionStorage:
    """Storage for BookVersion model - converts between ORM and domain models."""

    def __init__(self, session: AsyncSession):
        """Initialize book version repository."""
        self.session = session

    def _to_domain(self, orm: Optional[BookVersionORM]) -> Optional[BookVersionModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return BookVersionModel.model_validate(orm)

    async def create(self, **kwargs: Any) -> BookVersionModel:
        """Create a new book version."""
        try:
            orm_version = BookVersionORM(**kwargs)
            self.session.add(orm_version)
            await self.session.flush()
            await self.session.refresh(orm_version)
            result = self._to_domain(orm_version)
            if result is None:
                raise ValueError("Failed to create book version model")
            return result
        except SQLAlchemyError:
            raise

    async def get_by_isbn(self, isbn: str) -> Optional[BookVersionModel]:
        """Get book version by ISBN."""
        try:
            stmt = select(BookVersionORM).where(BookVersionORM.isbn == isbn)
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def get_by_book_id(
        self, book_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[BookVersionModel]:
        """Get versions by book ID."""
        try:
            stmt = (
                select(BookVersionORM)
                .where(BookVersionORM.book_id == book_id)
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


class PublisherStorage:
    """Storage for Publisher model - converts between ORM and domain models."""

    def __init__(self, session: AsyncSession):
        """Initialize publisher repository."""
        self.session = session

    def _to_domain(self, orm: Optional[PublisherORM]) -> Optional[PublisherModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return PublisherModel.model_validate(orm)

    async def create(self, **kwargs: Any) -> PublisherModel:
        """Create a new publisher."""
        try:
            orm_publisher = PublisherORM(**kwargs)
            self.session.add(orm_publisher)
            await self.session.flush()
            await self.session.refresh(orm_publisher)
            result = self._to_domain(orm_publisher)
            if result is None:
                raise ValueError("Failed to create publisher model")
            return result
        except SQLAlchemyError:
            raise

    async def get_by_id(self, publisher_id: UUID) -> Optional[PublisherModel]:
        """Get publisher by ID."""
        try:
            stmt = select(PublisherORM).where(PublisherORM.id == publisher_id)
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def get_by_name(self, name: str) -> Optional[PublisherModel]:
        """Get publisher by name."""
        try:
            stmt = select(PublisherORM).where(PublisherORM.name == name)
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise
