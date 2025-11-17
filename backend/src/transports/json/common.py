"""Common schemas used across all entities."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TimestampMixin(BaseModel):
    """Mixin for created_at and updated_at timestamps."""

    created_at: datetime
    updated_at: datetime


class IDResponse(BaseModel):
    """Response schema with just an ID."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)
