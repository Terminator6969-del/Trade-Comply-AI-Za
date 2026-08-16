"""
FastAPI dependency injection helpers for authentication and authorization.
Used with Depends() in route handlers.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError

from app.core.database import get_async_session
from app.core.security import decode_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User, Organization, Membership


async def get_current_user(token: Annotated[str, None] = None) -> dict:
    """
    Extract and validate JWT token, return user claims.
    
    Raises:
        HTTPException: If token is missing or invalid
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )

    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        org_id: str = payload.get("org_id")

        if not user_id or not org_id:
            raise ValueError("Token missing required claims")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {"user_id": user_id, "org_id": org_id}


async def get_user_from_db(
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> User:
    """
    Get User object from database using token claims.
    Verifies user exists and is active.
    
    Raises:
        HTTPException: If user not found or inactive
    """
    result = await session.execute(select(User).where(User.id == claims["user_id"]))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user


async def get_org_from_db(
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Organization:
    """
    Get Organization object from database using token claims.
    Verifies user has membership in org.
    
    Raises:
        HTTPException: If org not found or user not member
    """
    # Verify membership
    result = await session.execute(
        select(Membership).where(
            Membership.user_id == claims["user_id"],
            Membership.organization_id == claims["org_id"],
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not member of organization",
        )

    # Get organization
    result = await session.execute(select(Organization).where(Organization.id == claims["org_id"]))
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return org


async def get_current_org_id(
    claims: Annotated[dict, Depends(get_current_user)],
) -> str:
    """
    Get organization ID from token claims.
    Used for filtering queries by org_id.
    """
    return claims["org_id"]


async def check_role(required_role: str):
    """
    Factory for role-based access control.
    
    Usage in routes:
        @router.get("/admin")
        async def admin_route(
            user: User = Depends(check_role("admin"))
        ):
            ...
    """

    async def _check_role(
        claims: Annotated[dict, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ) -> User:
        user = await get_user_from_db(claims, session)

        # Get user's role in org
        result = await session.execute(
            select(Membership).where(
                Membership.user_id == user.id,
                Membership.organization_id == claims["org_id"],
            )
        )
        membership = result.scalar_one_or_none()

        if not membership or membership.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role}",
            )

        return user

    return _check_role
