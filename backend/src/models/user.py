"""User models for authentication and user management."""
import uuid
from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import BaseModel


class UserModel(PydanticBaseModel):
    """Application/domain model for user information."""
    id: uuid.UUID
    username: str
    email: str
    full_name: str | None = None
    is_active: bool = True

    class Config:
        from_attributes = True


class UserORM(BaseModel):
    """User model for storing user information."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    security = relationship(
        "UserSecurityORM",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    refresh_tokens = relationship(
        "RefreshTokenModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    clubs = relationship(
        "ClubORM",
        secondary="user_clubs",
        back_populates="members"
    )
    pages = relationship(
        "PageORM",
        secondary="user_pages",
        back_populates="followers"
    )

class UserSecurityModel(PydanticBaseModel):
    """Application/domain model for user security information."""
    user_id: uuid.UUID
    email: str
    password: str
    old_password: str | None = None
    password_changed_at: datetime | None = None

    class Config:
        from_attributes = True


class UserSecurityORM(BaseModel):
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
    user = relationship("UserORM", back_populates="security")
