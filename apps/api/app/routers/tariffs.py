"""
Tariff records API routes for searching and viewing South African HS codes.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user
from app.models import TariffRecord
from app.schemas.tariff import TariffRecordResponse
from app.services.classification_service import search_tariffs

router = APIRouter(prefix="/api/v1/tariffs", tags=["tariffs"])


@router.get("/search", response_model=list[TariffRecordResponse])
async def search_tariffs_endpoint(
    q: str = Query(..., min_length=1, description="Search query (description, 4/6/8-digit HS code)"),
    limit: int = Query(default=20, ge=1, le=100),
    claims: Annotated[dict, Depends(get_current_user)] = None,
    session: Annotated[AsyncSession, Depends(get_async_session)] = None,
) -> list[TariffRecordResponse]:
    """
    Search South African Schedule 1 tariff records with descriptions and duty rates.
    """
    tariffs = await search_tariffs(session, q, limit)
    return [
        TariffRecordResponse(
            id=str(t.id),
            hs_code=t.hs_code,
            sa_tariff_code=t.sa_tariff_code,
            description=t.description,
            duty_rate=t.duty_rate,
            vat_rate=t.vat_rate,
            unit_of_measure=t.unit_of_measure,
            chapter=t.chapter,
            section=t.section,
        )
        for t in tariffs
    ]


@router.get("/{hs_code}", response_model=TariffRecordResponse)
async def get_tariff_by_hs_code(
    hs_code: str,
    claims: Annotated[dict, Depends(get_current_user)] = None,
    session: Annotated[AsyncSession, Depends(get_async_session)] = None,
) -> TariffRecordResponse:
    """
    Look up a single tariff code by HS code (e.g., '8541.40' or '854140').
    """
    search_pattern = hs_code.strip()
    result = await session.execute(
        select(TariffRecord).where(
            (TariffRecord.hs_code == search_pattern)
            | (TariffRecord.sa_tariff_code == search_pattern)
            | (TariffRecord.hs_code.ilike(f"{search_pattern}%"))
        ).limit(1)
    )
    tariff = result.scalar_one_or_none()
    if not tariff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tariff code {hs_code} not found in database",
        )

    return TariffRecordResponse(
        id=str(tariff.id),
        hs_code=tariff.hs_code,
        sa_tariff_code=tariff.sa_tariff_code,
        description=tariff.description,
        duty_rate=tariff.duty_rate,
        vat_rate=tariff.vat_rate,
        unit_of_measure=tariff.unit_of_measure,
        chapter=tariff.chapter,
        section=tariff.section,
    )
