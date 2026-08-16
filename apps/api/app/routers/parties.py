"""
Party API routes for CRUD operations with pagination.
All endpoints are scoped to the authenticated organization.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user, get_org_from_db
from app.models import User, Party
from app.schemas.party import (
    PartyCreate,
    PartyUpdate,
    PartyResponse,
    PartyListResponse,
)
from app.services.party_service import (
    get_party,
    list_parties,
    create_party,
    update_party,
    delete_party,
    get_parties_by_type,
)

router = APIRouter(prefix="/api/v1/parties", tags=["parties"])


@router.get("", response_model=PartyListResponse)
async def list_parties_endpoint(
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    party_type: str | None = Query(None, description="Filter by party type"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
) -> PartyListResponse:
    """
    List parties with pagination and optional type filter.
    
    Args:
        organization: Current organization
        session: Database session
        party_type: Optional filter by party type
        page: Page number (1-indexed)
        per_page: Items per page (max 100)
        
    Returns:
        Paginated list of parties
    """
    parties, total = await list_parties(
        session,
        organization["id"],
        party_type=party_type,
        page=page,
        per_page=per_page,
    )
    
    return PartyListResponse(
        items=[PartyResponse.model_validate(p) for p in parties],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page,
    )


@router.post("", response_model=PartyResponse, status_code=status.HTTP_201_CREATED)
async def create_party_endpoint(
    request: PartyCreate,
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> PartyResponse:
    """
    Create a new party.
    
    Args:
        request: Party creation data
        organization: Current organization
        session: Database session
        
    Returns:
        Created party
    """
    party = await create_party(session, organization["id"], request)
    return PartyResponse.model_validate(party)


@router.get("/{party_id}", response_model=PartyResponse)
async def get_party_endpoint(
    party_id: str,
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> PartyResponse:
    """
    Get a party by ID.
    
    Args:
        party_id: Party ID
        organization: Current organization
        session: Database session
        
    Returns:
        Party details
    """
    party = await get_party(session, party_id, organization["id"])
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Party not found",
        )
    return PartyResponse.model_validate(party)


@router.patch("/{party_id}", response_model=PartyResponse)
async def update_party_endpoint(
    party_id: str,
    request: PartyUpdate,
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> PartyResponse:
    """
    Update a party.
    
    Args:
        party_id: Party ID
        request: Update data
        organization: Current organization
        session: Database session
        
    Returns:
        Updated party
    """
    party = await update_party(session, party_id, organization["id"], request)
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Party not found",
        )
    return PartyResponse.model_validate(party)


@router.delete("/{party_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_party_endpoint(
    party_id: str,
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    """
    Delete a party.
    
    Args:
        party_id: Party ID
        organization: Current organization
        session: Database session
    """
    deleted = await delete_party(session, party_id, organization["id"])
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Party not found",
        )


@router.get("/types/{party_type}", response_model=list[PartyResponse])
async def get_parties_by_type_endpoint(
    party_type: str,
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[PartyResponse]:
    """
    Get all parties of a specific type (for dropdowns/selection).
    
    Args:
        party_type: Party type (importer, exporter, supplier, etc.)
        organization: Current organization
        session: Database session
        
    Returns:
        List of parties of the specified type
    """
    parties = await get_parties_by_type(session, organization["id"], party_type)
    return [PartyResponse.model_validate(p) for p in parties]
