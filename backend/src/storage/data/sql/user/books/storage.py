"""Storage layer for user book library operations."""
from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import select, and_, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.book import (
    UserBookModel,
    UserBookORM,
    ReadingListModel,
    ReadingListORM,
    ReadingListItemModel,
    ReadingListItemORM,
)
from src.models.base import utc_now


class UserBookStorage:
    """Storage for user's book library - manages user's personal books."""

    def __init__(self, session: AsyncSession):
        """Initialize user book repository."""
        self.session = session

    def _to_domain(self, orm: Optional[UserBookORM]) -> Optional[UserBookModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return UserBookModel.model_validate(orm)

    async def create(
        self,
        user_id: UUID,
        book_id: UUID,
        book_version_id: UUID | None = None,
        **kwargs: Any
    ) -> UserBookModel:
        """
        Add a book to user's library.

        Args:
            user_id: The user's ID.
            book_id: The book's ID.
            book_version_id: Optional specific version/edition ID.
            **kwargs: Additional fields (rating, review, notes, etc.)

        Returns:
            UserBookModel: The created user book.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        try:
            orm_user_book = UserBookORM(
                user_id=user_id,
                book_id=book_id,
                book_version_id=book_version_id,
                added_date=kwargs.get('added_date', utc_now()),
                is_read=kwargs.get('is_read', False),
                read_date=kwargs.get('read_date'),
                rating=kwargs.get('rating'),
                review=kwargs.get('review'),
                notes=kwargs.get('notes'),
                is_favorite=kwargs.get('is_favorite', False),
            )
            self.session.add(orm_user_book)
            await self.session.flush()
            await self.session.refresh(orm_user_book)
            result = self._to_domain(orm_user_book)
            if result is None:
                raise ValueError("Failed to create user book")
            return result
        except SQLAlchemyError:
            raise

    async def get_by_id(self, user_book_id: UUID) -> Optional[UserBookModel]:
        """Get a user book by ID."""
        try:
            stmt = select(UserBookORM).where(UserBookORM.id == user_book_id)
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def get_user_book(
        self,
        user_id: UUID,
        book_id: UUID
    ) -> Optional[UserBookModel]:
        """Get a specific book from user's library."""
        try:
            stmt = select(UserBookORM).where(
                and_(
                    UserBookORM.user_id == user_id,
                    UserBookORM.book_id == book_id
                )
            )
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def get_user_library(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        is_read: bool | None = None,
        is_favorite: bool | None = None,
        min_rating: float | None = None
    ) -> List[UserBookModel]:
        """
        Get all books in user's library with optional filters.

        Args:
            user_id: The user's ID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            is_read: Filter by read status.
            is_favorite: Filter by favorite status.
            min_rating: Minimum rating filter.

        Returns:
            List[UserBookModel]: List of user's books.
        """
        try:
            stmt = select(UserBookORM).where(UserBookORM.user_id == user_id)

            # Apply filters
            if is_read is not None:
                stmt = stmt.where(UserBookORM.is_read == is_read)
            if is_favorite is not None:
                stmt = stmt.where(UserBookORM.is_favorite == is_favorite)
            if min_rating is not None:
                stmt = stmt.where(UserBookORM.rating >= min_rating)

            # Order by added date (most recent first)
            stmt = stmt.order_by(desc(UserBookORM.added_date)).offset(skip).limit(limit)

            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise

    async def update(
        self,
        user_book_id: UUID,
        **kwargs: Any
    ) -> Optional[UserBookModel]:
        """
        Update a user book (mark as read, add rating/review/notes, etc.).

        Args:
            user_book_id: The user book ID.
            **kwargs: Fields to update.

        Returns:
            Optional[UserBookModel]: Updated user book or None if not found.
        """
        try:
            orm_user_book = await self.session.get(UserBookORM, user_book_id)
            if orm_user_book:
                for key, value in kwargs.items():
                    if hasattr(orm_user_book, key):
                        setattr(orm_user_book, key, value)
                await self.session.flush()
                await self.session.refresh(orm_user_book)
            return self._to_domain(orm_user_book)
        except SQLAlchemyError:
            raise

    async def delete(self, user_book_id: UUID) -> bool:
        """Remove a book from user's library."""
        try:
            orm_user_book = await self.session.get(UserBookORM, user_book_id)
            if orm_user_book:
                await self.session.delete(orm_user_book)
                await self.session.flush()
                return True
            return False
        except SQLAlchemyError:
            raise

    async def mark_as_read(
        self,
        user_book_id: UUID,
        read_date: datetime | None = None
    ) -> Optional[UserBookModel]:
        """Mark a book as read."""
        return await self.update(
            user_book_id,
            is_read=True,
            read_date=read_date or utc_now()
        )

    async def mark_as_unread(self, user_book_id: UUID) -> Optional[UserBookModel]:
        """Mark a book as unread."""
        return await self.update(
            user_book_id,
            is_read=False,
            read_date=None,
            reading_status='reading'
        )

    async def set_reading_status(
        self,
        user_book_id: UUID,
        reading_status: str
    ) -> Optional[UserBookModel]:
        """Set reading status for a book."""
        # Update is_read and read_date based on status
        updates = {"reading_status": reading_status}

        if reading_status == 'finished':
            updates['is_read'] = True
            updates['read_date'] = utc_now()
        else:
            updates['is_read'] = False
            updates['read_date'] = None

        return await self.update(user_book_id, **updates)

    async def add_rating(
        self,
        user_book_id: UUID,
        rating: float
    ) -> Optional[UserBookModel]:
        """Add or update rating for a book."""
        if not 0.0 <= rating <= 5.0:
            raise ValueError("Rating must be between 0.0 and 5.0")
        return await self.update(user_book_id, rating=rating)

    async def add_review(
        self,
        user_book_id: UUID,
        review: str
    ) -> Optional[UserBookModel]:
        """Add or update review for a book."""
        return await self.update(user_book_id, review=review)

    async def add_notes(
        self,
        user_book_id: UUID,
        notes: str
    ) -> Optional[UserBookModel]:
        """Add or update notes for a book."""
        return await self.update(user_book_id, notes=notes)

    async def toggle_favorite(
        self,
        user_book_id: UUID
    ) -> Optional[UserBookModel]:
        """Toggle favorite status of a book."""
        user_book_orm = await self.session.get(UserBookORM, user_book_id)
        if user_book_orm:
            return await self.update(
                user_book_id,
                is_favorite=not user_book_orm.is_favorite
            )
        return None


class ReadingListStorage:
    """Storage for user's reading lists."""

    def __init__(self, session: AsyncSession):
        """Initialize reading list repository."""
        self.session = session

    def _to_domain(self, orm: Optional[ReadingListORM]) -> Optional[ReadingListModel]:
        """Convert ORM model to domain model."""
        if orm is None:
            return None
        return ReadingListModel.model_validate(orm)

    def _item_to_domain(
        self,
        orm: Optional[ReadingListItemORM]
    ) -> Optional[ReadingListItemModel]:
        """Convert ORM model to domain model for items."""
        if orm is None:
            return None
        return ReadingListItemModel.model_validate(orm)

    async def create(
        self,
        user_id: UUID,
        name: str,
        description: str | None = None,
        is_default: bool = False
    ) -> ReadingListModel:
        """Create a new reading list for a user."""
        try:
            orm_list = ReadingListORM(
                user_id=user_id,
                name=name,
                description=description,
                created_date=utc_now(),
                is_default=is_default
            )
            self.session.add(orm_list)
            await self.session.flush()
            await self.session.refresh(orm_list)
            result = self._to_domain(orm_list)
            if result is None:
                raise ValueError("Failed to create reading list")
            return result
        except SQLAlchemyError:
            raise

    async def get_by_id(self, reading_list_id: UUID) -> Optional[ReadingListModel]:
        """Get a reading list by ID."""
        try:
            stmt = select(ReadingListORM).where(ReadingListORM.id == reading_list_id)
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def get_user_reading_lists(
        self,
        user_id: UUID
    ) -> List[ReadingListModel]:
        """Get all reading lists for a user."""
        try:
            stmt = select(ReadingListORM).where(
                ReadingListORM.user_id == user_id
            ).order_by(desc(ReadingListORM.is_default), ReadingListORM.created_date)
            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise

    async def get_default_list(self, user_id: UUID) -> Optional[ReadingListModel]:
        """Get user's default reading list."""
        try:
            stmt = select(ReadingListORM).where(
                and_(
                    ReadingListORM.user_id == user_id,
                    ReadingListORM.is_default == True  # noqa: E712
                )
            )
            result = await self.session.execute(stmt)
            return self._to_domain(result.scalar_one_or_none())
        except SQLAlchemyError:
            raise

    async def update(
        self,
        reading_list_id: UUID,
        **kwargs: Any
    ) -> Optional[ReadingListModel]:
        """Update a reading list."""
        try:
            orm_list = await self.session.get(ReadingListORM, reading_list_id)
            if orm_list:
                for key, value in kwargs.items():
                    if hasattr(orm_list, key):
                        setattr(orm_list, key, value)
                await self.session.flush()
                await self.session.refresh(orm_list)
            return self._to_domain(orm_list)
        except SQLAlchemyError:
            raise

    async def delete(self, reading_list_id: UUID) -> bool:
        """Delete a reading list."""
        try:
            orm_list = await self.session.get(ReadingListORM, reading_list_id)
            if orm_list:
                await self.session.delete(orm_list)
                await self.session.flush()
                return True
            return False
        except SQLAlchemyError:
            raise

    async def add_book_to_list(
        self,
        reading_list_id: UUID,
        user_book_id: UUID,
        order_index: int | None = None
    ) -> ReadingListItemModel:
        """Add a book to a reading list."""
        try:
            # If no order specified, add to end
            if order_index is None:
                stmt = select(ReadingListItemORM).where(
                    ReadingListItemORM.reading_list_id == reading_list_id
                ).order_by(desc(ReadingListItemORM.order_index))
                result = await self.session.execute(stmt)
                last_item = result.scalar_one_or_none()
                order_index = (last_item.order_index + 1) if last_item else 0

            orm_item = ReadingListItemORM(
                reading_list_id=reading_list_id,
                user_book_id=user_book_id,
                order_index=order_index,
                added_date=utc_now()
            )
            self.session.add(orm_item)
            await self.session.flush()
            await self.session.refresh(orm_item)
            result = self._item_to_domain(orm_item)
            if result is None:
                raise ValueError("Failed to add book to reading list")
            return result
        except SQLAlchemyError:
            raise

    async def remove_book_from_list(
        self,
        reading_list_id: UUID,
        user_book_id: UUID
    ) -> bool:
        """Remove a book from a reading list."""
        try:
            stmt = select(ReadingListItemORM).where(
                and_(
                    ReadingListItemORM.reading_list_id == reading_list_id,
                    ReadingListItemORM.user_book_id == user_book_id
                )
            )
            result = await self.session.execute(stmt)
            item = result.scalar_one_or_none()
            if item:
                await self.session.delete(item)
                await self.session.flush()
                return True
            return False
        except SQLAlchemyError:
            raise

    async def get_list_items(
        self,
        reading_list_id: UUID
    ) -> List[ReadingListItemModel]:
        """Get all items in a reading list (in order)."""
        try:
            stmt = select(ReadingListItemORM).where(
                ReadingListItemORM.reading_list_id == reading_list_id
            ).order_by(ReadingListItemORM.order_index)
            result = await self.session.execute(stmt)
            return [
                domain for orm in result.scalars().all()
                if (domain := self._item_to_domain(orm)) is not None
            ]
        except SQLAlchemyError:
            raise

    async def reorder_items(
        self,
        items: List[tuple[UUID, int]]  # List of (item_id, new_order)
    ) -> bool:
        """Reorder items in a reading list."""
        try:
            for item_id, new_order in items:
                item = await self.session.get(ReadingListItemORM, item_id)
                if item:
                    item.order_index = new_order
            await self.session.flush()
            return True
        except SQLAlchemyError:
            raise
