"""Base model class with common fields."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def utc_now():
    """Return current UTC time as timezone-naive datetime for database storage."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class BaseModel(Base):
    """Base model with common fields for all entities."""

    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False
    )
