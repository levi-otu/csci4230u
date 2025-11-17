"""Page models for discussion topics."""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import Base, BaseModel

# Association table for user-page many-to-many relationship
user_pages = Table(
    "user_pages",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("page_id", UUID(as_uuid=True), ForeignKey("pages.id"), primary_key=True),
    Column("join_date", DateTime, default=datetime.utcnow, nullable=False),
)


class Page(BaseModel):
    """Page model for discussion topics (Reddit-style)."""

    __tablename__ = "pages"

    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    topic = Column(String(255), nullable=True, index=True)
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    followers = relationship(
        "User",
        secondary=user_pages,
        back_populates="pages"
    )
    creator = relationship("User", foreign_keys=[created_by])
