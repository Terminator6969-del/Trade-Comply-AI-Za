"""
Classification API routes for HS code classification.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_async_session
from app.core.dependencies import get_current_user
from app.services.classification_service import (
    search_tariffs,
    classify_line_item,
    classify_shipment,
    get_classification_candidates,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/classification", tags=["classification"])


@router.get("/tariffs/search", response_model=list[dict])
async def search_tariff_codes(
    q: str,
    limit: int = 10,
    claims: Annotated[dict, Depends(get_current_user)] = None,
    session: Annotated[AsyncSession, Depends(get_async_session)] = None,
):
    """
    Search tariff records by description or HS code.
    
    Args:
        q: Search query
        limit: Maximum results
        claims: Current user claims
        session: Database session
        
    Returns:
        List of matching tariff records
    """
    tariffs = await search_tariffs(session, q, limit)
    return [
        {
            "hs_code": t.hs_code,
            "sa_tariff_code": t.sa_tariff_code,
            "description": t.description,
            "duty_rate": t.duty_rate,
            "vat_rate": t.vat_rate,
        }
        for t in tariffs
    ]


@router.post("/line-items/{line_item_id}/classify", response_model=list[dict])
async def classify_single_line_item(
    line_item_id: str,
    description: str,
    claims: Annotated[dict, Depends(get_current_user)] = None,
    session: Annotated[AsyncSession, Depends(get_async_session)] = None,
):
    """
    Classify a single line item to HS codes.
    
    Args:
        line_item_id: Line item ID
        description: Product description
        claims: Current user claims
        session: Database session
        
    Returns:
        List of HS code candidates with confidence scores
    """
    candidates = await classify_line_item(
        session=session,
        line_item_id=line_item_id,
        description=description,
    )
    return [
        {
            "hs_code": c.hs_code,
            "sa_tariff_code": c.sa_tariff_code,
            "confidence": c.confidence,
            "reasoning": c.reasoning,
            "duty_rate": c.duty_rate,
            "vat_rate": c.vat_rate,
            "permit_flags": c.permit_flags,
        }
        for c in candidates
    ]


@router.post("/shipments/{shipment_id}/classify", response_model=dict)
async def classify_all_line_items(
    shipment_id: str,
    claims: Annotated[dict, Depends(get_current_user)] = None,
    session: Annotated[AsyncSession, Depends(get_async_session)] = None,
):
    """
    Classify all line items in a shipment.
    
    Args:
        shipment_id: Shipment ID
        claims: Current user claims
        session: Database session
        
    Returns:
        Dictionary mapping line_item_id to classification candidates
    """
    results = await classify_shipment(session, shipment_id)
    return {
        line_item_id: [
            {
                "hs_code": c.hs_code,
                "sa_tariff_code": c.sa_tariff_code,
                "confidence": c.confidence,
                "reasoning": c.reasoning,
                "duty_rate": c.duty_rate,
                "vat_rate": c.vat_rate,
                "permit_flags": c.permit_flags,
            }
            for c in candidates
        ]
        for line_item_id, candidates in results.items()
    }


@router.get("/line-items/{line_item_id}/candidates", response_model=list[dict])
async def get_candidates(
    line_item_id: str,
    limit: int = 5,
    claims: Annotated[dict, Depends(get_current_user)] = None,
    session: Annotated[AsyncSession, Depends(get_async_session)] = None,
):
    """
    Get classification candidates for a line item.
    
    Args:
        line_item_id: Line item ID
        limit: Maximum candidates
        claims: Current user claims
        session: Database session
        
    Returns:
        List of classification candidates
    """
    candidates = await get_classification_candidates(session, line_item_id, limit)
    return [
        {
            "hs_code": c.hs_code,
            "sa_tariff_code": c.sa_tariff_code,
            "confidence": c.confidence,
            "reasoning": c.reasoning,
            "duty_rate": c.duty_rate,
            "vat_rate": c.vat_rate,
            "permit_flags": c.permit_flags,
        }
        for c in candidates
    ]


@router.get("/")
async def classify():
    """Classify - To be implemented in Phase 3"""
    return {"message": "Classification endpoint - Coming soon"}
