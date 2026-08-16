"""
Test suite for authentication and security.
Tests password hashing, token generation, and auth flows.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_token,
)
from app.services.auth_service import register_user, login_user
from app.schemas.auth import RegisterRequest, LoginRequest


def test_password_hashing():
    """Test Argon2 password hashing."""
    password = "TestPassword123"
    hashed = get_password_hash(password)

    # Hashed password should not equal plain password
    assert hashed != password

    # Verify password should return True
    assert verify_password(password, hashed) is True

    # Wrong password should return False
    assert verify_password("WrongPassword", hashed) is False


def test_create_and_decode_access_token():
    """Test JWT token creation and decoding."""
    data = {"sub": "user-id", "org_id": "org-id"}
    token = create_access_token(data)

    # Token should be a string
    assert isinstance(token, str)
    assert len(token) > 0

    # Should be able to decode it
    decoded = decode_token(token)
    assert decoded["sub"] == "user-id"
    assert decoded["org_id"] == "org-id"


def test_decode_invalid_token():
    """Test that invalid token raises error."""
    from jose import JWTError

    invalid_token = "invalid.token.here"

    with pytest.raises(JWTError):
        decode_token(invalid_token)


@pytest.mark.asyncio
async def test_register_user(async_session: AsyncSession):
    """Test user registration flow."""
    request = RegisterRequest(
        email="newuser@example.com",
        password="SecurePass123",
        full_name="New User",
        organization_name="Test Org",
    )

    user, organization, tokens = await register_user(async_session, request)

    # Verify user was created
    assert user.id is not None
    assert user.email == "newuser@example.com"
    assert user.full_name == "New User"
    assert user.is_active is True

    # Verify organization was created
    assert organization.id is not None
    assert organization.name == "Test Org"
    assert organization.plan == "free"

    # Verify tokens were generated
    assert tokens.access_token is not None
    assert tokens.refresh_token is not None
    assert tokens.token_type == "bearer"
    assert tokens.expires_in > 0

    # Verify we can decode the access token
    decoded = decode_token(tokens.access_token)
    assert decoded["sub"] == user.id
    assert decoded["org_id"] == organization.id


@pytest.mark.asyncio
async def test_register_duplicate_email(async_session: AsyncSession, mock_user_data):
    """Test that duplicate email registration fails."""
    # Register first user
    request1 = RegisterRequest(
        email="duplicate@example.com",
        password="Pass123456",
        full_name="User One",
    )
    await register_user(async_session, request1)

    # Try to register with same email
    request2 = RegisterRequest(
        email="duplicate@example.com",
        password="DifferentPass123",
        full_name="User Two",
    )

    with pytest.raises(ValueError, match="already exists"):
        await register_user(async_session, request2)


@pytest.mark.asyncio
async def test_login_user(async_session: AsyncSession):
    """Test user login flow."""
    # First register a user
    register_req = RegisterRequest(
        email="login@example.com",
        password="LoginPass123",
        full_name="Login User",
    )
    user, organization, _ = await register_user(async_session, register_req)

    # Now login
    login_req = LoginRequest(
        email="login@example.com",
        password="LoginPass123",
    )
    logged_in_user, logged_in_org, tokens = await login_user(async_session, login_req)

    # Verify same user and org returned
    assert logged_in_user.id == user.id
    assert logged_in_org.id == organization.id

    # Verify tokens are valid
    decoded = decode_token(tokens.access_token)
    assert decoded["sub"] == user.id
    assert decoded["org_id"] == organization.id


@pytest.mark.asyncio
async def test_login_wrong_password(async_session: AsyncSession):
    """Test login with wrong password fails."""
    # Register user
    register_req = RegisterRequest(
        email="wrong@example.com",
        password="CorrectPass123",
        full_name="Wrong Pass User",
    )
    await register_user(async_session, register_req)

    # Try to login with wrong password
    login_req = LoginRequest(
        email="wrong@example.com",
        password="WrongPass456",
    )

    with pytest.raises(ValueError, match="Incorrect password"):
        await login_user(async_session, login_req)


@pytest.mark.asyncio
async def test_login_nonexistent_user(async_session: AsyncSession):
    """Test login for non-existent user fails."""
    login_req = LoginRequest(
        email="nonexistent@example.com",
        password="AnyPass123",
    )

    with pytest.raises(ValueError, match="not found"):
        await login_user(async_session, login_req)


if __name__ == "__main__":
    print("Run with: pytest apps/api/tests/test_auth.py -v")
