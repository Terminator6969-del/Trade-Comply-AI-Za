"""
Duties API routes for South African Customs duty and Import VAT estimation.
All endpoints are scoped to the authenticated organization.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user
from app.services.duty_service import calculate_shipment_duties
from app.schemas.duty import DutyEstimateRequest, DutyEstimateResponse

router = APIRouter(prefix="/api/v1/duties", tags=["duties"])


@router.post("/shipments/{shipment_id}/estimate", response_model=DutyEstimateResponse)
async def estimate_shipment_duties(
    shipment_id: str,
    request: DutyEstimateRequest,
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> DutyEstimateResponse:
    """
    Calculate South African Customs Duty, SARS Added Tax Value (ATV), and Import VAT for a shipment.
    """
    try:
        return await calculate_shipment_duties(
            session=session,
            org_id=claims["org_id"],
            shipment_id=shipment_id,
            exchange_rate=request.exchange_rate,
            customs_markup_percent=request.customs_markup_percent,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/shipments/{shipment_id}", response_model=DutyEstimateResponse)
async def get_shipment_duties(
    shipment_id: str,
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> DutyEstimateResponse:
    """
    Get duty & VAT estimation for a shipment using default indicative exchange rates.
    """
    try:
        return await calculate_shipment_duties(
            session=session,
            org_id=claims["org_id"],
            shipment_id=shipment_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
