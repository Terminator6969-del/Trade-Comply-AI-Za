"""
Authentication API routes for user registration and login.
Endpoints: POST /auth/register, POST /auth/login
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, UserResponse, OrganizationResponse, TokenResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AuthResponse:
    """
    Register a new user and create organization.
    
    Requires:
        - Unique email address
        - Password with 8+ characters
        - Full name
        
    Returns:
        User, Organization, and JWT tokens
    """
    try:
        user, organization, tokens = await register_user(session, request)
        
        return AuthResponse(
            user=UserResponse.model_validate(user),
            organization=OrganizationResponse.model_validate(organization),
            tokens=tokens,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AuthResponse:
    """
    Login user with email and password.
    
    Returns:
        User, Organization, and JWT tokens
    """
    try:
        user, organization, tokens = await login_user(session, request)
        
        return AuthResponse(
            user=UserResponse.model_validate(user),
            organization=OrganizationResponse.model_validate(organization),
            tokens=tokens,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )
