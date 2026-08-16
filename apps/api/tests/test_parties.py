"""
Test suite for party management.
Tests CRUD operations with multi-tenant isolation.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, User, Membership, Party
from app.schemas.party import PartyCreate, PartyUpdate
from app.services.party_service import (
    create_party,
    get_party,
    list_parties,
    update_party,
    delete_party,
)


@pytest.fixture
async def test_org_and_user(async_session: AsyncSession):
    """Create a test organization and user."""
    org = Organization(name="Test Org", slug="test-org-parties", plan="free")
    async_session.add(org)
    await async_session.flush()

    user = User(
        email="partyowner@test.com",
        password_hash="hashed",
        full_name="Party Owner",
    )
    async_session.add(user)
    await async_session.flush()

    membership = Membership(
        organization_id=org.id,
        user_id=user.id,
        role="owner",
    )
    async_session.add(membership)
    await async_session.commit()

    return org, user


@pytest.mark.asyncio
async def test_create_party(async_session: AsyncSession, test_org_and_user):
    """Test creating a party."""
    org, _ = test_org_and_user

    request = PartyCreate(
        party_type="importer",
        name="ABC Trading Co.",
        vat_number="4123456789",
        customs_code="1234567",
        address="123 Main St, Cape Town",
        contact_email="contact@abctrading.co.za",
        contact_phone="+27 21 555 1234",
    )

    party = await create_party(async_session, org.id, request)

    assert party.id is not None
    assert party.organization_id == org.id
    assert party.party_type == "importer"
    assert party.name == "ABC Trading Co."
    assert party.vat_number == "4123456789"
    assert party.customs_code == "1234567"


@pytest.mark.asyncio
async def test_get_party(async_session: AsyncSession, test_org_and_user):
    """Test retrieving a party."""
    org, _ = test_org_and_user

    request = PartyCreate(party_type="exporter", name="Export Co.")
    party = await create_party(async_session, org.id, request)

    retrieved = await get_party(async_session, org.id, party.id)
    assert retrieved is not None
    assert retrieved.name == "Export Co."
    assert retrieved.party_type == "exporter"


@pytest.mark.asyncio
async def test_get_party_not_found(async_session: AsyncSession, test_org_and_user):
    """Test retrieving non-existent party returns None."""
    org, _ = test_org_and_user

    result = await get_party(async_session, org.id, "nonexistent-id")
    assert result is None


@pytest.mark.asyncio
async def test_list_parties(async_session: AsyncSession, test_org_and_user):
    """Test listing parties."""
    org, _ = test_org_and_user

    # Create multiple parties
    await create_party(async_session, org.id, PartyCreate(party_type="importer", name="Importer A"))
    await create_party(async_session, org.id, PartyCreate(party_type="exporter", name="Exporter B"))
    await create_party(async_session, org.id, PartyCreate(party_type="supplier", name="Supplier C"))

    parties = await list_parties(async_session, org.id)
    assert len(parties) == 3

    # Filter by type
    importers = await list_parties(async_session, org.id, party_type="importer")
    assert len(importers) == 1
    assert importers[0].name == "Importer A"


@pytest.mark.asyncio
async def test_list_parties_with_limit_offset(async_session: AsyncSession, test_org_and_user):
    """Test pagination on party listing."""
    org, _ = test_org_and_user

    for i in range(5):
        await create_party(async_session, org.id, PartyCreate(party_type="importer", name=f"Party {i}"))

    # Get first 2
    page1 = await list_parties(async_session, org.id, limit=2, offset=0)
    assert len(page1) == 2

    # Get next 2
    page2 = await list_parties(async_session, org.id, limit=2, offset=2)
    assert len(page2) == 2


@pytest.mark.asyncio
async def test_update_party(async_session: AsyncSession, test_org_and_user):
    """Test updating a party."""
    org, _ = test_org_and_user

    request = PartyCreate(party_type="importer", name="Original Name")
    party = await create_party(async_session, org.id, request)

    update_req = PartyUpdate(name="Updated Name", vat_number="9876543210")
    updated = await update_party(async_session, org.id, party.id, update_req)

    assert updated is not None
    assert updated.name == "Updated Name"
    assert updated.vat_number == "9876543210"


@pytest.mark.asyncio
async def test_update_party_not_found(async_session: AsyncSession, test_org_and_user):
    """Test updating non-existent party returns None."""
    org, _ = test_org_and_user

    update_req = PartyUpdate(name="Updated Name")
    result = await update_party(async_session, org.id, "nonexistent-id", update_req)
    assert result is None


@pytest.mark.asyncio
async def test_delete_party(async_session: AsyncSession, test_org_and_user):
    """Test deleting a party."""
    org, _ = test_org_and_user

    request = PartyCreate(party_type="importer", name="To Delete")
    party = await create_party(async_session, org.id, request)

    deleted = await delete_party(async_session, org.id, party.id)
    assert deleted is True

    # Verify it's gone
    retrieved = await get_party(async_session, org.id, party.id)
    assert retrieved is None


@pytest.mark.asyncio
async def test_delete_party_not_found(async_session: AsyncSession, test_org_and_user):
    """Test deleting non-existent party returns False."""
    org, _ = test_org_and_user

    deleted = await delete_party(async_session, org.id, "nonexistent-id")
    assert deleted is False


@pytest.mark.asyncio
async def test_party_multi_tenant_isolation(async_session: AsyncSession):
    """Test that parties are isolated between organizations."""
    # Create two orgs
    org1 = Organization(name="Org 1", slug="org-1-parties", plan="free")
    org2 = Organization(name="Org 2", slug="org-2-parties", plan="free")
    async_session.add_all([org1, org2])
    await async_session.flush()

    # Create party in org1
    request = PartyCreate(party_type="importer", name="Org 1 Party")
    party1 = await create_party(async_session, org1.id, request)

    # Try to get party from org2 (should not find it)
    result = await get_party(async_session, org2.id, party1.id)
    assert result is None

    # List parties in org2 (should be empty)
    parties = await list_parties(async_session, org2.id)
    assert len(parties) == 0


@pytest.mark.asyncio
async def test_party_validation_invalid_type(async_session: AsyncSession, test_org_and_user):
    """Test that invalid party_type is rejected."""
    org, _ = test_org_and_user

    with pytest.raises(Exception):  # ValidationError
        PartyCreate(party_type="invalid_type", name="Test")


if __name__ == "__main__":
    print("Run with: pytest apps/api/tests/test_parties.py -v")
