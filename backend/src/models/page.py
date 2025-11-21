"""Page models for discussion topics."""
import uuid
from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import Base, BaseModel, utc_now

# Association table for user-page many-to-many relationship
user_pages = Table(
    "user_pages",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("page_id", UUID(as_uuid=True), ForeignKey("pages.id"), primary_key=True),
    Column("join_date", DateTime, default=utc_now, nullable=False),
)


class PageModel(PydanticBaseModel):
    """Application/domain model for page information."""
    id: uuid.UUID
    name: str
    description: str | None = None
    topic: str | None = None
    created_by: uuid.UUID
    is_active: bool = True

    class Config:
        from_attributes = True


class PageORM(BaseModel):
    """ORM model for discussion topics (Reddit-style)."""

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
        "UserORM",
        secondary=user_pages,
        back_populates="pages"
    )
    creator = relationship("UserORM", foreign_keys=[created_by])
