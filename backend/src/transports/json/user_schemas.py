"""User-related schemas."""
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    full_name: str | None = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    username: str | None = Field(None, min_length=3, max_length=255)
    email: EmailStr | None = None
    full_name: str | None = Field(None, max_length=255)
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: UUID
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(UserResponse):
    """Schema for detailed user response with relationships."""

    # Can add relationships here if needed
    pass
