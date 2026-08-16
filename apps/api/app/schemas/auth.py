"""
Pydantic schemas for authentication request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """User registration request."""

    email: EmailStr = Field(..., description="Email address")
    password: str = Field(
        ..., min_length=8, description="Password (min 8 chars, must include uppercase, lowercase, digit)"
    )
    full_name: str = Field(..., min_length=2, description="Full name")
    organization_name: str | None = Field(None, description="Organization name (creates new org if provided)")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123",
                "full_name": "John Doe",
                "organization_name": "Acme Corp",
            }
        }


class LoginRequest(BaseModel):
    """User login request."""

    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")

    class Config:
        """Pydantic config."""

        json_schema_extra = {"example": {"email": "user@example.com", "password": "SecurePassword123"}}


class TokenResponse(BaseModel):
    """Token response after successful login."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiration in seconds")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
            }
        }


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""

    refresh_token: str = Field(..., description="JWT refresh token")


class UserResponse(BaseModel):
    """User response model."""

    id: str = Field(..., description="User ID")
    email: str = Field(..., description="Email address")
    full_name: str = Field(..., description="Full name")
    is_active: bool = Field(..., description="Whether user is active")

    class Config:
        """Pydantic config."""

        from_attributes = True


class OrganizationResponse(BaseModel):
    """Organization response model."""

    id: str = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    slug: str = Field(..., description="Organization slug")
    plan: str = Field(..., description="Subscription plan")

    class Config:
        """Pydantic config."""

        from_attributes = True


class AuthResponse(BaseModel):
    """Complete authentication response with user and org."""

    user: UserResponse = Field(..., description="User info")
    organization: OrganizationResponse = Field(..., description="Organization info")
    tokens: TokenResponse = Field(..., description="Access tokens")
