"""Book-related schemas."""
from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.transports.json.common import TimestampMixin


class PublisherBase(BaseModel):
    """Base publisher schema."""

    name: str = Field(..., min_length=1, max_length=255)
    country: str | None = Field(None, max_length=100)
    website: str | None = Field(None, max_length=500)


class PublisherCreate(PublisherBase):
    """Schema for creating a publisher."""

    pass


class PublisherUpdate(BaseModel):
    """Schema for updating a publisher."""

    name: str | None = Field(None, min_length=1, max_length=255)
    country: str | None = Field(None, max_length=100)
    website: str | None = Field(None, max_length=500)


class PublisherResponse(PublisherBase, TimestampMixin):
    """Schema for publisher response."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    """Base book schema."""

    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)
    date_of_first_publish: date | None = None
    genre: str | None = Field(None, max_length=100)
    description: str | None = None


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


class BookResponse(BookBase, TimestampMixin):
    """Schema for book response."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class BookVersionBase(BaseModel):
    """Base book version schema."""

    isbn: str = Field(..., min_length=10, max_length=13)
    publish_date: date | None = None
    edition: str | None = Field(None, max_length=100)
    editors: str | None = Field(None, max_length=500)
    editor_info: str | None = None


class BookVersionCreate(BookVersionBase):
    """Schema for creating a book version."""

    book_id: UUID
    publisher_id: UUID | None = None


class BookVersionUpdate(BaseModel):
    """Schema for updating a book version."""

    isbn: str | None = Field(None, min_length=10, max_length=13)
    publish_date: date | None = None
    edition: str | None = Field(None, max_length=100)
    editors: str | None = Field(None, max_length=500)
    editor_info: str | None = None
    publisher_id: UUID | None = None


class BookVersionResponse(BookVersionBase, TimestampMixin):
    """Schema for book version response."""

    id: UUID
    book_id: UUID
    publisher_id: UUID | None

    model_config = ConfigDict(from_attributes=True)
