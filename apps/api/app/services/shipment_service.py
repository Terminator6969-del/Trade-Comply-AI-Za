"""
Shipment service for managing shipments.
"""

from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Shipment, Party
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate


async def get_shipment(
    session: AsyncSession,
    shipment_id: str,
    organization_id: str,
) -> Shipment | None:
    """Get shipment by ID within organization."""
    result = await session.execute(
        select(Shipment).where(
            Shipment.id == shipment_id,
            Shipment.organization_id == organization_id,
        )
    )
    return result.scalar_one_or_none()


async def list_shipments(
    session: AsyncSession,
    organization_id: str,
    status: str | None = None,
    risk_level: str | None = None,
    shipment_type: str | None = None,
    search: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[Shipment], int]:
    """List shipments with pagination and filters."""
    query = select(Shipment).where(Shipment.organization_id == organization_id)
    
    if status:
        query = query.where(Shipment.status == status)
    if risk_level:
        query = query.where(Shipment.risk_level == risk_level)
    if shipment_type:
        query = query.where(Shipment.shipment_type == shipment_type)
    if search:
        query = query.where(
            or_(
                Shipment.reference.ilike(f"%{search}%"),
                Shipment.origin_country.ilike(f"%{search}%"),
                Shipment.destination_country.ilike(f"%{search}%"),
            )
        )
    
    # Get total count
    count_query = query.with_only_columns(select(Shipment.id).count())
    total = await session.scalar(count_query)
    
    # Apply pagination
    query = query.order_by(Shipment.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await session.execute(query)
    shipments = result.scalars().all()
    
    return shipments, total


async def create_shipment(
    session: AsyncSession,
    organization_id: str,
    request: ShipmentCreate,
    created_by: str | None = None,
) -> Shipment:
    """Create a new shipment."""
    # Validate referenced parties exist and belong to org
    party_ids = [
        request.importer_id,
        request.exporter_id,
        request.supplier_id,
        request.consignee_id,
        request.notify_party_id,
        request.clearing_agent_id,
    ]
    party_ids = [pid for pid in party_ids if pid is not None]

    if party_ids:
        result = await session.execute(
            select(Party).where(
                Party.id.in_(party_ids),
                Party.organization_id == organization_id,
            )
        )
        found_parties = result.scalars().all()
        found_ids = {p.id for p in found_parties}

        for pid in party_ids:
            if pid not in found_ids:
                raise ValueError(f"Party {pid} not found or not in organization")

    shipment = Shipment(
        organization_id=organization_id,
        created_by=created_by,
        **request.model_dump(),
    )
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)
    return shipment


async def update_shipment(
    session: AsyncSession,
    shipment_id: str,
    organization_id: str,
    request: ShipmentUpdate,
) -> Shipment | None:
    """Update a shipment."""
    shipment = await get_shipment(session, shipment_id, organization_id)
    if not shipment:
        return None
    
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(shipment, field, value)
    
    await session.commit()
    await session.refresh(shipment)
    return shipment


async def delete_shipment(
    session: AsyncSession,
    shipment_id: str,
    organization_id: str,
) -> bool:
    """Delete a shipment."""
    shipment = await get_shipment(session, shipment_id, organization_id)
    if not shipment:
        return False
    
    await session.delete(shipment)
    await session.commit()
    return True


async def get_shipments_by_status(
    session: AsyncSession,
    organization_id: str,
    status: str,
) -> list[Shipment]:
    """Get all shipments with a specific status."""
    result = await session.execute(
        select(Shipment).where(
            Shipment.organization_id == organization_id,
            Shipment.status == status,
        ).order_by(Shipment.created_at.desc())
    )
    return result.scalars().all()
    return True
