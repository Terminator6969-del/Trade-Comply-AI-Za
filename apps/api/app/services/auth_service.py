"""
Authentication service for user registration and login.
Handles password hashing, token generation, and org creation.
"""

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, create_refresh_token, get_password_hash
from app.models import Organization, User, Membership
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse, OrganizationResponse, TokenResponse
from app.core.config import settings


async def register_user(
    session: AsyncSession,
    request: RegisterRequest,
) -> tuple[User, Organization, TokenResponse]:
    """
    Register a new user and create organization.
    
    Args:
        session: Database session
        request: Registration request with email, password, name, org name
        
    Returns:
        Tuple of (User, Organization, TokenResponse)
        
    Raises:
        ValueError: If email already exists or org slug is taken
    """
    # Check if user with email already exists
    result = await session.execute(select(User).where(User.email == request.email))
    if result.scalar_one_or_none():
        raise ValueError(f"User with email {request.email} already exists")

    # Create organization
    org_name = request.organization_name or f"{request.full_name}'s Organization"
    org_slug = f"{org_name.lower().replace(' ', '-')}-{str(uuid4())[:8]}"

    # Check if slug is unique
    result = await session.execute(select(Organization).where(Organization.slug == org_slug))
    if result.scalar_one_or_none():
        raise ValueError(f"Organization slug {org_slug} already exists")

    organization = Organization(
        name=org_name,
        slug=org_slug,
        plan="free",
    )
    session.add(organization)
    await session.flush()  # Get org ID without committing

    # Create user with hashed password
    user = User(
        email=request.email,
        password_hash=get_password_hash(request.password),
        full_name=request.full_name,
        is_active=True,
    )
    session.add(user)
    await session.flush()  # Get user ID without committing

    # Create membership (owner role)
    membership = Membership(
        organization_id=organization.id,
        user_id=user.id,
        role="owner",
    )
    session.add(membership)
    await session.commit()

    # Generate tokens
    access_token_data = {"sub": user.id, "org_id": organization.id}
    access_token = create_access_token(access_token_data)
    refresh_token = create_refresh_token(access_token_data)

    token_response = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return user, organization, token_response


async def login_user(
    session: AsyncSession,
    request: LoginRequest,
) -> tuple[User, Organization, TokenResponse]:
    """
    Login user and return tokens.
    
    Args:
        session: Database session
        request: Login request with email and password
        
    Returns:
        Tuple of (User, Organization, TokenResponse)
        
    Raises:
        ValueError: If user not found or password incorrect
    """
    # Find user by email
    result = await session.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    if not user:
        raise ValueError(f"User with email {request.email} not found")

    if not user.is_active:
        raise ValueError("User account is inactive")

    # Verify password
    from app.core.security import verify_password

    if not verify_password(request.password, user.password_hash):
        raise ValueError("Incorrect password")

    # Get user's first organization (primary org)
    result = await session.execute(
        select(Organization)
        .join(Membership)
        .where(Membership.user_id == user.id)
    )
    organization = result.scalar_one_or_none()

    if not organization:
        raise ValueError("User has no organization assigned")

    # Generate tokens
    access_token_data = {"sub": user.id, "org_id": organization.id}
    access_token = create_access_token(access_token_data)
    refresh_token = create_refresh_token(access_token_data)

    token_response = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return user, organization, token_response
