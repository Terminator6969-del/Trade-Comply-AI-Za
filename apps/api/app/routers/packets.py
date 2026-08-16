"""
Customs SAD500 Packet generation router.
All endpoints are scoped to the authenticated organization.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user
from app.services.packet_service import generate_customs_packet
from app.schemas.packet import PacketGenerateRequest, PacketResponse

router = APIRouter(prefix="/api/v1/packets", tags=["packets"])


@router.post("/shipments/{shipment_id}/generate", response_model=PacketResponse)
async def generate_packet_endpoint(
    shipment_id: str,
    request: PacketGenerateRequest,
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> PacketResponse:
    """
    Generate a full Customs SAD500 packet in JSON, CSV, or Text Summary format.
    """
    try:
        return await generate_customs_packet(
            session=session,
            org_id=claims["org_id"],
            shipment_id=shipment_id,
            output_format=request.format,
            user_id=claims.get("sub"),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/shipments/{shipment_id}/download")
async def download_packet_csv(
    shipment_id: str,
    format: str = Query(default="csv", regex="^(csv|summary|json)$"),
    claims: Annotated[dict, Depends(get_current_user)] = None,
    session: Annotated[AsyncSession, Depends(get_async_session)] = None,
):
    """
    Download the generated customs packet file (CSV or text summary).
    """
    try:
        packet = await generate_customs_packet(
            session=session,
            org_id=claims["org_id"],
            shipment_id=shipment_id,
            output_format=format,
            user_id=claims.get("sub"),
        )
        if format == "csv":
            return Response(
                content=packet.raw_content or "",
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename=SAD500_{packet.reference}.csv"
                },
            )
        elif format == "summary":
            return Response(
                content=packet.raw_content or "",
                media_type="text/plain",
                headers={
                    "Content-Disposition": f"attachment; filename=SAD500_{packet.reference}.txt"
                },
            )
        return packet
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
