"""Authentication-related schemas."""
import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Schema for user registration."""

    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72, description="Password (max 72 characters due to bcrypt limitation)")
    full_name: str | None = Field(None, max_length=255)

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one symbol/special character
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/~`]', v):
            raise ValueError('Password must contain at least one symbol (!@#$%^&*(),.?":{}|<>_-+=[]\\\/~`)')

        return v


class LoginRequest(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes in seconds
    refresh_token: str | None = None  # Only used internally, not exposed in API


class TokenData(BaseModel):
    """Schema for token data payload."""

    user_id: str | None = None
