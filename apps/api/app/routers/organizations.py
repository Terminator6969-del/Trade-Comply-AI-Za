"""
Organization API routes for CRUD and membership management.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user, get_user_from_db, get_org_from_db
from app.models import User, Organization
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    MembershipResponse,
)
from app.services.organization_service import (
    create_organization,
    get_organization,
    update_organization,
    get_user_role_in_org,
)

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


@router.get("/me", response_model=OrganizationResponse)
async def get_current_organization(
    org: Annotated[Organization, Depends(get_org_from_db)],
) -> OrganizationResponse:
    """
    Get the current user's organization.
    
    Returns:
        Current organization details
    """
    return OrganizationResponse.model_validate(org)


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_org(
    request: OrganizationCreate,
    user: Annotated[User, Depends(get_user_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> OrganizationResponse:
    """
    Create a new organization.
    Authenticated user becomes the owner.
    
    Args:
        request: Organization creation details
        user: Current authenticated user
        session: Database session
        
    Returns:
        Created organization
    """
    try:
        org = await create_organization(session, request, user.id)
        return OrganizationResponse.model_validate(org)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create organization",
        )


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_org(
    org_id: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    claims: Annotated[dict, Depends(get_current_user)],
) -> OrganizationResponse:
    """
    Get organization details by ID.
    User must be member of the organization.
    
    Args:
        org_id: Organization ID
        session: Database session
        claims: Current user claims
        
    Returns:
        Organization details
    """
    # Verify user is member of org
    if claims["org_id"] != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    org = await get_organization(session, org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return OrganizationResponse.model_validate(org)


@router.patch("/{org_id}", response_model=OrganizationResponse)
async def update_org(
    org_id: str,
    request: OrganizationUpdate,
    user: Annotated[User, Depends(get_user_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    claims: Annotated[dict, Depends(get_current_user)],
) -> OrganizationResponse:
    """
    Update organization details.
    Only owners and admins can update org.
    
    Args:
        org_id: Organization ID
        request: Update details
        user: Current user
        session: Database session
        claims: Current user claims
        
    Returns:
        Updated organization
    """
    # Verify user is member of org
    if claims["org_id"] != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    # Check user has permission
    role = await get_user_role_in_org(session, user.id, org_id)
    if role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    org = await update_organization(session, org_id, request)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return OrganizationResponse.model_validate(org)
