"""Security module tests for coverage."""
from datetime import timedelta
from jose import jwt

from src.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    verify_token
)


def test_create_access_token():
    """Test access token creation."""
    user_id = "test-user-id"
    token = create_access_token(subject=user_id)
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_custom_expiry():
    """Test access token with custom expiry."""
    user_id = "test-user-id"
    token = create_access_token(subject=user_id, expires_delta=timedelta(minutes=30))
    assert isinstance(token, str)


def test_create_refresh_token():
    """Test refresh token creation."""
    user_id = "test-user-id"
    token, expiry = create_refresh_token(subject=user_id)
    assert isinstance(token, str)
    assert len(token) > 0
    assert expiry is not None


def test_create_refresh_token_custom_expiry():
    """Test refresh token with custom expiry."""
    user_id = "test-user-id"
    token, expiry = create_refresh_token(subject=user_id, expires_delta=timedelta(days=1))
    assert isinstance(token, str)
    assert expiry is not None


def test_password_hashing():
    """Test password hashing and verification."""
    password = "TestPassword123!"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_verify_valid_token():
    """Test verifying valid token."""
    user_id = "test-user-id"
    token = create_access_token(subject=user_id)

    payload = verify_token(token, "access")
    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["type"] == "access"


def test_verify_invalid_token():
    """Test verifying invalid token."""
    payload = verify_token("invalid.token.here", "access")
    assert payload is None


def test_verify_token_wrong_signature():
    """Test verifying token with wrong signature."""
    # Create a token with a different secret
    fake_token = jwt.encode(
        {"sub": "user123", "type": "access"},
        "wrong-secret-key",
        algorithm="HS256"
    )

    payload = verify_token(fake_token, "access")
    assert payload is None


def test_verify_password_incorrect():
    """Test password verification with incorrect password."""
    password = "CorrectPassword123!"
    hashed = get_password_hash(password)

    assert verify_password("IncorrectPassword123!", hashed) is False


def test_multiple_tokens_unique():
    """Test that multiple tokens are unique."""
    user_id = "test-user-id"

    token1 = create_refresh_token(subject=user_id)[0]
    token2 = create_refresh_token(subject=user_id)[0]

    # Tokens should be different due to jti
    assert token1 != token2


def test_access_token_contains_required_fields():
    """Test that access token contains required fields."""
    user_id = "test-user-id"
    token = create_access_token(subject=user_id)

    payload = verify_token(token, "access")
    assert "sub" in payload
    assert "exp" in payload
    assert "type" in payload
    assert payload["type"] == "access"


def test_refresh_token_contains_required_fields():
    """Test that refresh token contains required fields."""
    user_id = "test-user-id"
    token, _ = create_refresh_token(subject=user_id)

    payload = verify_token(token, "refresh")
    assert "sub" in payload
    assert "exp" in payload
    assert "type" in payload
    assert "jti" in payload
    assert payload["type"] == "refresh"
