"""Group models for organizing users."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import Base, BaseModel

# Association table for user-group many-to-many relationship
user_groups = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("group_id", UUID(as_uuid=True), ForeignKey("groups.id"), primary_key=True),
    Column("joined_at", DateTime, default=datetime.utcnow, nullable=False),
)


class Group(BaseModel):
    """Group model for organizing users by interests or topics."""

    __tablename__ = "groups"

    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    # Relationships
    users = relationship(
        "User",
        secondary=user_groups,
        back_populates="groups"
    )
    creator = relationship("User", foreign_keys=[created_by])
