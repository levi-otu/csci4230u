"""Book models for library management."""
import uuid
from datetime import date

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Column, Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


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

    # Relationships
    versions = relationship(
        "BookVersionORM",
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
