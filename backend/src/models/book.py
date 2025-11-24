"""Book models for library management."""
import uuid
from datetime import date, datetime

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import BaseModel, utc_now


class PublisherModel(PydanticBaseModel):
    """Application/domain model for publisher information."""
    id: uuid.UUID
    name: str
    country: str | None = None
    website: str | None = None

    class Config:
        from_attributes = True


class PublisherORM(BaseModel):
    """ORM model for book publishers."""

    __tablename__ = "publishers"

    name = Column(String(255), unique=True, nullable=False, index=True)
    country = Column(String(100), nullable=True)
    website = Column(String(500), nullable=True)

    # Relationships
    book_versions = relationship(
        "BookVersionORM",
        back_populates="publisher",
        cascade="all, delete-orphan"
    )


class BookModel(PydanticBaseModel):
    """Application/domain model for book information."""
    id: uuid.UUID
    title: str
    author: str
    date_of_first_publish: date | None = None
    genre: str | None = None
    description: str | None = None
    cover_image_url: str | None = None
    # Multi-volume series support
    series_title: str | None = None
    volume_number: int | None = None
    volume_title: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookORM(BaseModel):
    """ORM model for storing book information."""

    __tablename__ = "books"

    title = Column(String(500), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    date_of_first_publish = Column(Date, nullable=True)
    genre = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    cover_image_url = Column(String(1000), nullable=True)
    # Multi-volume series support
    series_title = Column(String(500), nullable=True)
    volume_number = Column(Integer, nullable=True)
    volume_title = Column(String(500), nullable=True)

    # Relationships
    versions = relationship(
        "BookVersionORM",
        back_populates="book",
        cascade="all, delete-orphan"
    )
    user_books = relationship(
        "UserBookORM",
        back_populates="book",
        cascade="all, delete-orphan"
    )


class BookVersionModel(PydanticBaseModel):
    """Application/domain model for book version information."""
    id: uuid.UUID
    book_id: uuid.UUID
    publisher_id: uuid.UUID | None = None
    isbn: str
    publish_date: date | None = None
    edition: str | None = None
    editors: str | None = None
    editor_info: str | None = None

    class Config:
        from_attributes = True


class BookVersionORM(BaseModel):
    """ORM model for different editions and publications."""

    __tablename__ = "book_versions"

    book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    publisher_id = Column(
        UUID(as_uuid=True),
        ForeignKey("publishers.id"),
        nullable=True,
        index=True
    )
    isbn = Column(String(13), unique=True, nullable=False, index=True)
    publish_date = Column(Date, nullable=True)
    edition = Column(String(100), nullable=True)
    editors = Column(String(500), nullable=True)
    editor_info = Column(Text, nullable=True)

    # Relationships
    book = relationship("BookORM", back_populates="versions")
    publisher = relationship("PublisherORM", back_populates="book_versions")


# User Library Models

class UserBookModel(PydanticBaseModel):
    """Application/domain model for user's book in their library."""
    id: uuid.UUID
    user_id: uuid.UUID
    book_id: uuid.UUID
    book_version_id: uuid.UUID | None = None
    added_date: datetime
    is_read: bool = False
    read_date: datetime | None = None
    reading_status: str = 'unread'  # 'unread', 'reading', 'finished'
    rating: float | None = None  # 0.0 to 5.0
    review: str | None = None
    notes: str | None = None
    is_favorite: bool = False

    class Config:
        from_attributes = True


class UserBookORM(BaseModel):
    """ORM model for user's book library."""

    __tablename__ = "user_books"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    book_version_id = Column(
        UUID(as_uuid=True),
        ForeignKey("book_versions.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    added_date = Column(DateTime, default=utc_now, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    read_date = Column(DateTime, nullable=True)
    reading_status = Column(String(20), default='unread', nullable=False)  # 'unread', 'reading', 'finished'
    rating = Column(Float, nullable=True)  # 0.0 to 5.0
    review = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    is_favorite = Column(Boolean, default=False, nullable=False)

    # Relationships
    book = relationship("BookORM", back_populates="user_books")
    book_version = relationship("BookVersionORM")
    reading_list_items = relationship(
        "ReadingListItemORM",
        back_populates="user_book",
        cascade="all, delete-orphan"
    )


class ReadingListModel(PydanticBaseModel):
    """Application/domain model for user's reading list."""
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: str | None = None
    created_date: datetime
    is_default: bool = False

    class Config:
        from_attributes = True


class ReadingListORM(BaseModel):
    """ORM model for user's reading lists."""

    __tablename__ = "reading_lists"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_date = Column(DateTime, default=utc_now, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    # Relationships
    items = relationship(
        "ReadingListItemORM",
        back_populates="reading_list",
        cascade="all, delete-orphan",
        order_by="ReadingListItemORM.order_index"
    )


class ReadingListItemModel(PydanticBaseModel):
    """Application/domain model for items in a reading list."""
    id: uuid.UUID
    reading_list_id: uuid.UUID
    user_book_id: uuid.UUID
    order_index: int
    added_date: datetime

    class Config:
        from_attributes = True


class ReadingListItemORM(BaseModel):
    """ORM model for reading list items (ordered)."""

    __tablename__ = "reading_list_items"

    reading_list_id = Column(
        UUID(as_uuid=True),
        ForeignKey("reading_lists.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_books.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    order_index = Column(Integer, nullable=False)
    added_date = Column(DateTime, default=utc_now, nullable=False)

    # Relationships
    reading_list = relationship("ReadingListORM", back_populates="items")
    user_book = relationship("UserBookORM", back_populates="reading_list_items")
