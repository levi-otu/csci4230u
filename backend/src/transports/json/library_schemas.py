"""Library-related schemas for API transport."""
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.transports.json.common import TimestampMixin


# Book Schemas

class BookBase(BaseModel):
    """Base book schema."""

    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)
    date_of_first_publish: date | None = None
    genre: str | None = Field(None, max_length=100)
    description: str | None = None
    cover_image_url: str | None = Field(None, max_length=1000)
    # Multi-volume series support
    series_title: str | None = Field(None, max_length=500)
    volume_number: int | None = None
    volume_title: str | None = Field(None, max_length=500)


class BookCreate(BookBase):
    """Schema for creating a book."""

    pass


class BookUpdate(BaseModel):
    """Schema for updating a book."""

    title: str | None = Field(None, min_length=1, max_length=500)
    author: str | None = Field(None, min_length=1, max_length=255)
    date_of_first_publish: date | None = None
    genre: str | None = Field(None, max_length=100)
    description: str | None = None
    cover_image_url: str | None = Field(None, max_length=1000)
    # Multi-volume series support
    series_title: str | None = Field(None, max_length=500)
    volume_number: int | None = None
    volume_title: str | None = Field(None, max_length=500)


class BookResponse(BookBase, TimestampMixin):
    """Schema for book response."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


# ISBN Lookup Schemas

class ISBNLookupRequest(BaseModel):
    """Request schema for ISBN lookup."""

    isbn: str = Field(..., min_length=10, max_length=13, pattern=r"^\d{10}(\d{3})?$")


class ISBNLookupResponse(BaseModel):
    """Response schema for ISBN lookup from external API."""

    found: bool
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    publish_date: str | None = None
    genre: str | None = None
    isbn_10: str | None = None
    isbn_13: str | None = None
    cover_url: str | None = None
    description: str | None = None
    page_count: int | None = None
    # Multi-volume series support
    series_title: str | None = None  # The overall series name (e.g., "Reformed Dogmatics")
    volume_number: int | None = None  # Which volume this is (e.g., 2)
    volume_title: str | None = None  # The subtitle for this volume (e.g., "God and creation")
    total_volumes: int | None = None  # Total volumes in the series (e.g., 4)


# User Book Schemas

class UserBookBase(BaseModel):
    """Base user book schema."""

    book_id: UUID
    book_version_id: UUID | None = None
    is_read: bool = False
    read_date: datetime | None = None
    reading_status: str = 'unread'  # 'unread', 'reading', 'finished'
    rating: float | None = Field(None, ge=0.0, le=5.0)
    review: str | None = None
    notes: str | None = None
    is_favorite: bool = False


class UserBookCreate(UserBookBase):
    """Schema for adding a book to user's library."""

    pass


class UserBookUpdate(BaseModel):
    """Schema for updating a user book."""

    is_read: bool | None = None
    read_date: datetime | None = None
    reading_status: str | None = None  # 'unread', 'reading', 'finished'
    rating: float | None = Field(None, ge=0.0, le=5.0)
    review: str | None = None
    notes: str | None = None
    is_favorite: bool | None = None


class UserBookResponse(UserBookBase):
    """Schema for user book response."""

    id: UUID
    user_id: UUID
    added_date: datetime
    # Nested book data for convenience
    book: BookResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class UserBookWithDetails(UserBookResponse):
    """Extended user book response with full book details."""

    book: BookResponse

    model_config = ConfigDict(from_attributes=True)


# Reading List Schemas

class ReadingListBase(BaseModel):
    """Base reading list schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    is_default: bool = False


class ReadingListCreate(ReadingListBase):
    """Schema for creating a reading list."""

    pass


class ReadingListUpdate(BaseModel):
    """Schema for updating a reading list."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


class ReadingListResponse(ReadingListBase):
    """Schema for reading list response."""

    id: UUID
    user_id: UUID
    created_date: datetime
    item_count: int = 0

    model_config = ConfigDict(from_attributes=True)


# Reading List Item Schemas

class ReadingListItemCreate(BaseModel):
    """Schema for adding a book to a reading list."""

    user_book_id: UUID
    order_index: int | None = None


class ReadingListItemResponse(BaseModel):
    """Schema for reading list item response."""

    id: UUID
    reading_list_id: UUID
    user_book_id: UUID
    order_index: int
    added_date: datetime
    # Nested user book data
    user_book: UserBookWithDetails | None = None

    model_config = ConfigDict(from_attributes=True)


class ReadingListWithItems(ReadingListResponse):
    """Extended reading list response with items."""

    items: list[ReadingListItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ReorderItemsRequest(BaseModel):
    """Request schema for reordering reading list items."""

    items: list[tuple[UUID, int]] = Field(
        ...,
        description="List of (item_id, new_order_index) tuples"
    )


# Quick Actions Schemas

class MarkAsReadRequest(BaseModel):
    """Request schema for marking a book as read."""

    read_date: datetime | None = None


class AddRatingRequest(BaseModel):
    """Request schema for adding/updating a rating."""

    rating: float = Field(..., ge=0.0, le=5.0)


class AddReviewRequest(BaseModel):
    """Request schema for adding/updating a review."""

    review: str = Field(..., min_length=1)


class AddNotesRequest(BaseModel):
    """Request schema for adding/updating notes."""

    notes: str = Field(..., min_length=1)


# Library Statistics

class LibraryStatsResponse(BaseModel):
    """Response schema for library statistics."""

    total_books: int
    read_books: int
    unread_books: int
    favorite_books: int
    total_reading_lists: int
    average_rating: float | None = None
    books_read_this_year: int = 0
    books_read_this_month: int = 0

    model_config = ConfigDict(from_attributes=True)
