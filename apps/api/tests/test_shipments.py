"""
Test suite for shipment management.
Tests CRUD operations with multi-tenant isolation and party validation.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, User, Membership, Party, Shipment
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.services.shipment_service import (
    create_shipment,
    get_shipment,
    list_shipments,
    update_shipment,
    delete_shipment,
)


@pytest.fixture
async def test_org_and_parties(async_session: AsyncSession):
    """Create a test organization with parties."""
    org = Organization(name="Test Org", slug="test-org-shipments", plan="free")
    async_session.add(org)
    await async_session.flush()

    user = User(
        email="shipmentowner@test.com",
        password_hash="hashed",
        full_name="Shipment Owner",
    )
    async_session.add(user)
    await async_session.flush()

    membership = Membership(
        organization_id=org.id,
        user_id=user.id,
        role="owner",
    )
    async_session.add(membership)

    # Create parties
    importer = Party(
        organization_id=org.id,
        party_type="importer",
        name="Test Importer",
    )
    exporter = Party(
        organization_id=org.id,
        party_type="exporter",
        name="Test Exporter",
    )
    async_session.add_all([importer, exporter])
    await async_session.commit()

    return org, user, importer, exporter


@pytest.mark.asyncio
async def test_create_shipment(async_session: AsyncSession, test_org_and_parties):
    """Test creating a shipment."""
    org, _, importer, exporter = test_org_and_parties

    request = ShipmentCreate(
        reference="SHIP-2026-001",
        shipment_type="import",
        importer_id=importer.id,
        exporter_id=exporter.id,
    )

    shipment = await create_shipment(async_session, org.id, request)

    assert shipment.id is not None
    assert shipment.organization_id == org.id
    assert shipment.reference == "SHIP-2026-001"
    assert shipment.shipment_type == "import"
    assert shipment.status == "draft"  # Default status
    assert shipment.risk_level == "low"  # Default risk level
    assert shipment.importer_id == importer.id
    assert shipment.exporter_id == exporter.id


@pytest.mark.asyncio
async def test_create_shipment_without_parties(async_session: AsyncSession, test_org_and_parties):
    """Test creating a shipment without party references."""
    org, _, _, _ = test_org_and_parties

    request = ShipmentCreate(
        reference="SHIP-2026-002",
        shipment_type="export",
    )

    shipment = await create_shipment(async_session, org.id, request)

    assert shipment.id is not None
    assert shipment.reference == "SHIP-2026-002"
    assert shipment.shipment_type == "export"
    assert shipment.importer_id is None
    assert shipment.exporter_id is None


@pytest.mark.asyncio
async def test_create_shipment_invalid_party(async_session: AsyncSession, test_org_and_parties):
    """Test that creating shipment with non-existent party fails."""
    org, _, _, _ = test_org_and_parties

    request = ShipmentCreate(
        reference="SHIP-2026-003",
        shipment_type="import",
        importer_id="nonexistent-party-id",
    )

    with pytest.raises(ValueError, match="not found"):
        await create_shipment(async_session, org.id, request)


@pytest.mark.asyncio
async def test_get_shipment(async_session: AsyncSession, test_org_and_parties):
    """Test retrieving a shipment."""
    org, _, importer, _ = test_org_and_parties

    request = ShipmentCreate(
        reference="SHIP-2026-001",
        shipment_type="import",
        importer_id=importer.id,
    )
    shipment = await create_shipment(async_session, org.id, request)

    retrieved = await get_shipment(async_session, org.id, shipment.id)
    assert retrieved is not None
    assert retrieved.reference == "SHIP-2026-001"
    assert retrieved.shipment_type == "import"


@pytest.mark.asyncio
async def test_get_shipment_not_found(async_session: AsyncSession, test_org_and_parties):
    """Test retrieving non-existent shipment returns None."""
    org, _, _, _ = test_org_and_parties

    result = await get_shipment(async_session, org.id, "nonexistent-id")
    assert result is None


@pytest.mark.asyncio
async def test_list_shipments(async_session: AsyncSession, test_org_and_parties):
    """Test listing shipments."""
    org, _, importer, _ = test_org_and_parties

    # Create multiple shipments
    await create_shipment(async_session, org.id, ShipmentCreate(reference="SHIP-001", shipment_type="import", importer_id=importer.id))
    await create_shipment(async_session, org.id, ShipmentCreate(reference="SHIP-002", shipment_type="export"))
    await create_shipment(async_session, org.id, ShipmentCreate(reference="SHIP-003", shipment_type="transit"))

    shipments, total = await list_shipments(async_session, org.id)
    assert len(shipments) == 3
    assert total == 3

    # Filter by type
    imports, import_count = await list_shipments(async_session, org.id, shipment_type="import")
    assert len(imports) == 1
    assert import_count == 1
    assert imports[0].reference == "SHIP-001"


@pytest.mark.asyncio
async def test_list_shipments_with_filters(async_session: AsyncSession, test_org_and_parties):
    """Test filtering shipments by status and risk level."""
    org, _, importer, _ = test_org_and_parties

    # Create shipments with different statuses
    s1 = await create_shipment(async_session, org.id, ShipmentCreate(reference="SHIP-001", shipment_type="import"))
    s2 = await create_shipment(async_session, org.id, ShipmentCreate(reference="SHIP-002", shipment_type="export"))

    # Update statuses
    await update_shipment(async_session, org.id, s1.id, ShipmentUpdate(status="submitted", risk_level="high"))
    await update_shipment(async_session, org.id, s2.id, ShipmentUpdate(status="approved", risk_level="low"))

    # Filter by status
    submitted, count = await list_shipments(async_session, org.id, status="submitted")
    assert len(submitted) == 1
    assert submitted[0].reference == "SHIP-001"

    # Filter by risk level
    high_risk, count = await list_shipments(async_session, org.id, risk_level="high")
    assert len(high_risk) == 1


@pytest.mark.asyncio
async def test_list_shipments_pagination(async_session: AsyncSession, test_org_and_parties):
    """Test pagination on shipment listing."""
    org, _, _, _ = test_org_and_parties

    for i in range(5):
        await create_shipment(async_session, org.id, ShipmentCreate(reference=f"SHIP-{i:03d}", shipment_type="import"))

    # Get first 2
    page1, total = await list_shipments(async_session, org.id, limit=2, offset=0)
    assert len(page1) == 2
    assert total == 5

    # Get next 2
    page2, _ = await list_shipments(async_session, org.id, limit=2, offset=2)
    assert len(page2) == 2


@pytest.mark.asyncio
async def test_update_shipment(async_session: AsyncSession, test_org_and_parties):
    """Test updating a shipment."""
    org, _, importer, _ = test_org_and_parties

    request = ShipmentCreate(reference="SHIP-2026-001", shipment_type="import")
    shipment = await create_shipment(async_session, org.id, request)

    update_req = ShipmentUpdate(status="submitted", risk_level="medium")
    updated = await update_shipment(async_session, org.id, shipment.id, update_req)

    assert updated is not None
    assert updated.status == "submitted"
    assert updated.risk_level == "medium"


@pytest.mark.asyncio
async def test_update_shipment_not_found(async_session: AsyncSession, test_org_and_parties):
    """Test updating non-existent shipment returns None."""
    org, _, _, _ = test_org_and_parties

    update_req = ShipmentUpdate(status="submitted")
    result = await update_shipment(async_session, org.id, "nonexistent-id", update_req)
    assert result is None


@pytest.mark.asyncio
async def test_delete_shipment(async_session: AsyncSession, test_org_and_parties):
    """Test deleting a shipment."""
    org, _, _, _ = test_org_and_parties

    request = ShipmentCreate(reference="SHIP-2026-001", shipment_type="import")
    shipment = await create_shipment(async_session, org.id, request)

    deleted = await delete_shipment(async_session, org.id, shipment.id)
    assert deleted is True

    # Verify it's gone
    retrieved = await get_shipment(async_session, org.id, shipment.id)
    assert retrieved is None


@pytest.mark.asyncio
async def test_delete_shipment_not_found(async_session: AsyncSession, test_org_and_parties):
    """Test deleting non-existent shipment returns False."""
    org, _, _, _ = test_org_and_parties

    deleted = await delete_shipment(async_session, org.id, "nonexistent-id")
    assert deleted is False


@pytest.mark.asyncio
async def test_shipment_multi_tenant_isolation(async_session: AsyncSession):
    """Test that shipments are isolated between organizations."""
    # Create two orgs
    org1 = Organization(name="Org 1", slug="org-1-shipments", plan="free")
    org2 = Organization(name="Org 2", slug="org-2-shipments", plan="free")
    async_session.add_all([org1, org2])
    await async_session.flush()

    # Create shipment in org1
    request = ShipmentCreate(reference="SHIP-ORG1-001", shipment_type="import")
    shipment1 = await create_shipment(async_session, org1.id, request)

    # Try to get shipment from org2 (should not find it)
    result = await get_shipment(async_session, org2.id, shipment1.id)
    assert result is None

    # List shipments in org2 (should be empty)
    shipments, total = await list_shipments(async_session, org2.id)
    assert len(shipments) == 0
    assert total == 0


@pytest.mark.asyncio
async def test_shipment_default_status_and_risk(async_session: AsyncSession, test_org_and_parties):
    """Test that new shipments get default status and risk level."""
    org, _, _, _ = test_org_and_parties

    request = ShipmentCreate(reference="SHIP-2026-001", shipment_type="import")
    shipment = await create_shipment(async_session, org.id, request)

    assert shipment.status == "draft"
    assert shipment.risk_level == "low"


if __name__ == "__main__":
    print("Run with: pytest apps/api/tests/test_shipments.py -v")
