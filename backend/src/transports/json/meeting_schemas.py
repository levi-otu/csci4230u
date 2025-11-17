"""Meeting-related schemas."""
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.transports.json.common import TimestampMixin


class MeetingBase(BaseModel):
    """Base meeting schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    scheduled_start: str  # ISO datetime string
    scheduled_end: str  # ISO datetime string
    duration: int = Field(..., gt=0)  # Duration in minutes


class MeetingCreate(MeetingBase):
    """Schema for creating a meeting."""

    club_id: UUID | None = None


class MeetingUpdate(BaseModel):
    """Schema for updating a meeting."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    status: str | None = Field(
        None,
        pattern="^(scheduled|in_progress|completed|cancelled)$"
    )
    scheduled_start: str | None = None
    scheduled_end: str | None = None
    actual_start: str | None = None
    actual_end: str | None = None
    duration: int | None = Field(None, gt=0)


class MeetingResponse(MeetingBase, TimestampMixin):
    """Schema for meeting response."""

    id: UUID
    status: str
    actual_start: str | None
    actual_end: str | None
    created_by: UUID
    club_id: UUID | None

    model_config = ConfigDict(from_attributes=True)
