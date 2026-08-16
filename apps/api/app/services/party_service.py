"""
Party service for managing trade parties.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Party
from app.schemas.party import PartyCreate, PartyUpdate


async def get_party(
    session: AsyncSession,
    party_id: str,
    organization_id: str,
) -> Party | None:
    """Get party by ID within organization."""
    result = await session.execute(
        select(Party).where(
            Party.id == party_id,
            Party.organization_id == organization_id,
        )
    )
    return result.scalar_one_or_none()


async def list_parties(
    session: AsyncSession,
    organization_id: str,
    party_type: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> tuple[list[Party], int]:
    """List parties with pagination and optional type filter."""
    query = select(Party).where(Party.organization_id == organization_id)
    
    if party_type:
        query = query.where(Party.party_type == party_type)
    
    # Get total count
    count_query = query.with_only_columns(select(Party.id).count())
    total = await session.scalar(count_query)
    
    # Apply pagination
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await session.execute(query)
    parties = result.scalars().all()
    
    return parties, total


async def create_party(
    session: AsyncSession,
    organization_id: str,
    request: PartyCreate,
) -> Party:
    """Create a new party."""
    party = Party(
        organization_id=organization_id,
        **request.model_dump(),
    )
    session.add(party)
    await session.commit()
    await session.refresh(party)
    return party


async def update_party(
    session: AsyncSession,
    party_id: str,
    organization_id: str,
    request: PartyUpdate,
) -> Party | None:
    """Update a party."""
    party = await get_party(session, party_id, organization_id)
    if not party:
        return None
    
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(party, field, value)
    
    await session.commit()
    await session.refresh(party)
    return party


async def delete_party(
    session: AsyncSession,
    party_id: str,
    organization_id: str,
) -> bool:
    """Delete a party."""
    party = await get_party(session, party_id, organization_id)
    if not party:
        return False
    
    await session.delete(party)
    await session.commit()
    return True


async def get_parties_by_type(
    session: AsyncSession,
    organization_id: str,
    party_type: str,
) -> list[Party]:
    """Get all parties of a specific type for dropdowns/selection."""
    result = await session.execute(
        select(Party).where(
            Party.organization_id == organization_id,
            Party.party_type == party_type,
        ).order_by(Party.name)
    )
    return result.scalars().all()


async def update_party(
    session: AsyncSession,
    org_id: str,
    party_id: str,
    request: PartyUpdate,
) -> Party | None:
    """
    Update a party, scoped to organization.
    
    Args:
        session: Database session
        org_id: Organization ID (multi-tenant isolation)
        party_id: Party ID
        request: Update data
        
    Returns:
        Updated Party or None if not found
    """
    party = await get_party(session, org_id, party_id)
    if not party:
        return None

    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(party, field, value)

    await session.commit()
    await session.refresh(party)
    return party


async def delete_party(
    session: AsyncSession,
    org_id: str,
    party_id: str,
) -> bool:
    """
    Delete a party, scoped to organization.
    
    Args:
        session: Database session
        org_id: Organization ID (multi-tenant isolation)
        party_id: Party ID
        
    Returns:
        True if deleted, False if not found
    """
    party = await get_party(session, org_id, party_id)
    if not party:
        return False

    await session.delete(party)
    await session.commit()
    return True
