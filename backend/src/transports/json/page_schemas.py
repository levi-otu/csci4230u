"""Page-related schemas."""
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.transports.json.common import TimestampMixin


class PageBase(BaseModel):
    """Base page schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    topic: str | None = Field(None, max_length=255)


class PageCreate(PageBase):
    """Schema for creating a page."""

    pass


class PageUpdate(BaseModel):
    """Schema for updating a page."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    topic: str | None = Field(None, max_length=255)
    is_active: bool | None = None


class PageResponse(PageBase, TimestampMixin):
    """Schema for page response."""

    id: UUID
    created_by: UUID
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
