"""
Shipments API routes for CRUD operations with pagination.
All endpoints are scoped to the authenticated organization.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user, get_org_from_db
from app.models import User, Shipment
from app.schemas.shipment import (
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentResponse,
    ShipmentListResponse,
)
from app.services.shipment_service import (
    create_shipment,
    get_shipment,
    list_shipments,
    update_shipment,
    delete_shipment,
)

router = APIRouter(prefix="/api/v1/shipments", tags=["shipments"])


@router.post("", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment_endpoint(
    request: ShipmentCreate,
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ShipmentResponse:
    """
    Create a new shipment.
    
    Args:
        request: Shipment creation data
        organization: Current organization
        session: Database session
        
    Returns:
        Created shipment
        
    Raises:
        HTTPException: 400 if referenced party not found
    """
    try:
        shipment = await create_shipment(session, organization["id"], request)
        return ShipmentResponse.model_validate(shipment)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("", response_model=ShipmentListResponse)
async def list_shipments_endpoint(
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    status: str | None = Query(None, description="Filter by status"),
    risk_level: str | None = Query(None, description="Filter by risk level"),
    shipment_type: str | None = Query(None, description="Filter by shipment type"),
    search: str | None = Query(None, description="Search reference or country"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
) -> ShipmentListResponse:
    """
    List shipments with pagination and filters.
    
    Args:
        organization: Current organization
        session: Database session
        status: Optional filter by status
        risk_level: Optional filter by risk level
        shipment_type: Optional filter by shipment type
        search: Optional search term
        page: Page number (1-indexed)
        per_page: Items per page (max 100)
        
    Returns:
        Paginated list of shipments
    """
    shipments, total = await list_shipments(
        session,
        organization["id"],
        status=status,
        risk_level=risk_level,
        shipment_type=shipment_type,
        search=search,
        page=page,
        per_page=per_page,
    )
    
    return ShipmentListResponse(
        items=[ShipmentResponse.model_validate(s) for s in shipments],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page,
    )


@router.get("/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment_endpoint(
    shipment_id: str,
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ShipmentResponse:
    """
    Get a shipment by ID.
    
    Args:
        shipment_id: Shipment ID
        organization: Current organization
        session: Database session
        
    Returns:
        Shipment details
    """
    shipment = await get_shipment(session, shipment_id, organization["id"])
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    return ShipmentResponse.model_validate(shipment)


@router.patch("/{shipment_id}", response_model=ShipmentResponse)
async def update_shipment_endpoint(
    shipment_id: str,
    request: ShipmentUpdate,
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ShipmentResponse:
    """
    Update a shipment.
    
    Args:
        shipment_id: Shipment ID
        request: Update data
        organization: Current organization
        session: Database session
        
    Returns:
        Updated shipment
    """
    shipment = await update_shipment(session, shipment_id, organization["id"], request)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    return ShipmentResponse.model_validate(shipment)


@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment_endpoint(
    shipment_id: str,
    organization: Annotated[dict, Depends(get_org_from_db)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> None:
    """
    Delete a shipment.
    
    Args:
        shipment_id: Shipment ID
        organization: Current organization
        session: Database session
    """
    deleted = await delete_shipment(session, shipment_id, organization["id"])
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
