"""Schema validation tests to increase coverage."""
import pytest
from pydantic import ValidationError

from src.transports.json.auth_schemas import RegisterRequest


def test_password_validation_no_uppercase():
    """Test password validation - missing uppercase."""
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(
            username="testuser",
            email="test@example.com",
            password="testpass123!",
            full_name="Test User"
        )
    assert "uppercase" in str(exc_info.value).lower()


def test_password_validation_no_lowercase():
    """Test password validation - missing lowercase."""
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(
            username="testuser",
            email="test@example.com",
            password="TESTPASS123!",
            full_name="Test User"
        )
    assert "lowercase" in str(exc_info.value).lower()


def test_password_validation_no_symbol():
    """Test password validation - missing symbol."""
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(
            username="testuser",
            email="test@example.com",
            password="TestPass123",
            full_name="Test User"
        )
    assert "symbol" in str(exc_info.value).lower()


def test_password_validation_too_short():
    """Test password validation - too short."""
    with pytest.raises(ValidationError) as exc_info:
        RegisterRequest(
            username="testuser",
            email="test@example.com",
            password="Tp1!",
            full_name="Test User"
        )
    # Either "8" or "characters" should appear in the error
    error_str = str(exc_info.value).lower()
    assert "8" in error_str or "characters" in error_str


def test_valid_password():
    """Test valid password passes validation."""
    request = RegisterRequest(
        username="testuser",
        email="test@example.com",
        password="ValidPass123!",
        full_name="Test User"
    )
    assert request.password == "ValidPass123!"


def test_password_with_various_symbols():
    """Test password validation with different symbols."""
    symbols = "!@#$%^&*(),.?\":{}|<>_-+=[]\\/~`"
    for symbol in symbols:
        password = f"TestPass123{symbol}"
        request = RegisterRequest(
            username="testuser",
            email="test@example.com",
            password=password,
            full_name="Test User"
        )
        assert request.password == password
