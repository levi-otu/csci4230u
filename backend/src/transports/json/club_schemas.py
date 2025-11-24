"""Club-related schemas."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.transports.json.common import TimestampMixin


class ClubBase(BaseModel):
    """Base club schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    topic: str | None = Field(None, max_length=255)
    max_members: int | None = Field(None, gt=0)


class ClubCreate(ClubBase):
    """Schema for creating a club."""

    pass


class ClubUpdate(BaseModel):
    """Schema for updating a club."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    topic: str | None = Field(None, max_length=255)
    is_active: bool | None = None
    max_members: int | None = Field(None, gt=0)


class ClubResponse(ClubBase, TimestampMixin):
    """Schema for club response."""

    id: UUID
    name: str
    description: str | None
    created_by: UUID
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ClubMeetingBase(BaseModel):
    """Base club meeting schema."""

    start_date: str  # ISO datetime string
    end_date: str | None = None
    frequency: str = Field(..., pattern="^(once|daily|weekly|monthly)$")
    recurrence_rule: str | None = Field(None, max_length=500)


class ClubMeetingCreate(ClubMeetingBase):
    """Schema for creating a club meeting."""

    meeting_id: UUID


class ClubMeetingUpdate(BaseModel):
    """Schema for updating a club meeting."""

    start_date: str | None = None
    end_date: str | None = None
    frequency: str | None = Field(None, pattern="^(once|daily|weekly|monthly)$")
    recurrence_rule: str | None = Field(None, max_length=500)


class ClubMeetingResponse(ClubMeetingBase, TimestampMixin):
    """Schema for club meeting response."""

    id: UUID
    club_id: UUID
    meeting_id: UUID

    model_config = ConfigDict(from_attributes=True)


class AddUserToClub(BaseModel):
    """Schema for adding a user to a club."""

    user_id: UUID
    role: str = Field(default="member", pattern="^(member|owner)$")


class UserClubResponse(BaseModel):
    """Schema for user-club membership response."""

    user_id: UUID
    club_id: UUID
    join_date: datetime
    role: str

    model_config = ConfigDict(from_attributes=True)
