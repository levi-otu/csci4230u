"""Role models for RBAC (Role-Based Access Control)."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import Base, BaseModel

# Association table for user-role many-to-many relationship
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True),
    Column("assigned_at", DateTime, default=datetime.utcnow, nullable=False),
)


class Role(BaseModel):
    """Role model for defining user roles and permissions."""

    __tablename__ = "roles"

    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=True)

    # Relationships
    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles"
    )
