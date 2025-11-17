"""Book models for library management."""
import uuid

from sqlalchemy import Column, Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class Publisher(BaseModel):
    """Publisher model for book publishers."""

    __tablename__ = "publishers"

    name = Column(String(255), unique=True, nullable=False, index=True)
    country = Column(String(100), nullable=True)
    website = Column(String(500), nullable=True)

    # Relationships
    book_versions = relationship(
        "BookVersion",
        back_populates="publisher",
        cascade="all, delete-orphan"
    )


class Book(BaseModel):
    """Book model for storing book information."""

    __tablename__ = "books"

    title = Column(String(500), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    date_of_first_publish = Column(Date, nullable=True)
    genre = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    versions = relationship(
        "BookVersion",
        back_populates="book",
        cascade="all, delete-orphan"
    )


class BookVersion(BaseModel):
    """Book version model for different editions and publications."""

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
    book = relationship("Book", back_populates="versions")
    publisher = relationship("Publisher", back_populates="book_versions")
