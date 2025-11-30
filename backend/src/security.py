"""Security utilities for JWT authentication and password hashing."""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Bcrypt has a 72-byte limit, so passwords are truncated to 72 bytes.

    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to verify against.

    Returns:
        bool: True if password matches, False otherwise.
    """
    # Truncate password to 72 bytes for bcrypt compatibility
    truncated_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(truncated_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    Bcrypt has a 72-byte limit, so passwords are truncated to 72 bytes.

    Args:
        password: The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    # Truncate password to 72 bytes for bcrypt compatibility
    truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(truncated_password)


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        subject: The subject of the token (usually user ID).
        expires_delta: Optional custom expiration time.

    Returns:
        str: The encoded JWT token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> tuple[str, datetime]:
    """
    Create a JWT refresh token.

    Args:
        subject: The subject of the token (usually user ID).
        expires_delta: Optional custom expiration time.

    Returns:
        tuple[str, datetime]: The encoded JWT refresh token and expiration time.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    # Add jti (JWT ID) claim for uniqueness to prevent hash collisions
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
        "jti": str(uuid.uuid4())
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt, expire


def verify_token(token: str, token_type: str | None = None) -> Optional[dict[str, Any]]:
    """
    Verify and decode a JWT token.

    Args:
        token: The JWT token to verify.
        token_type: Optional token type to verify ("access" or "refresh").

    Returns:
        Optional[dict]: The decoded token payload if valid, None otherwise.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Verify token type if specified
        if token_type and payload.get("type") != token_type:
            return None

        return payload
    except JWTError:
        return None
