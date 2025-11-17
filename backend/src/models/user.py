"""User models for authentication and user management."""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class User(BaseModel):
    """User model for storing user information."""

    __tablename__ = "users"

    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    security = relationship(
        "UserSecurity",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users"
    )
    groups = relationship(
        "Group",
        secondary="user_groups",
        back_populates="users"
    )
    clubs = relationship(
        "Club",
        secondary="user_clubs",
        back_populates="members"
    )
    pages = relationship(
        "Page",
        secondary="user_pages",
        back_populates="followers"
    )


class UserSecurity(BaseModel):
    """User security model for storing authentication credentials."""

    __tablename__ = "user_security"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    old_password = Column(String(255), nullable=True)
    password_changed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="security")
