"""
Test suite for organization management and RBAC.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Organization, Membership
from app.schemas.organization import OrganizationCreate
from app.services.organization_service import (
    create_organization,
    get_organization,
    update_organization,
    get_user_role_in_org,
    add_member_to_org,
    remove_member_from_org,
)
from app.models import User


@pytest.mark.asyncio
async def test_create_organization(async_session: AsyncSession, mock_user_data):
    """Test creating an organization."""
    # Create a user first
    user = User(
        email="orgowner@example.com",
        password_hash="hash",
        full_name="Org Owner",
    )
    async_session.add(user)
    await async_session.flush()

    # Create organization
    req = OrganizationCreate(name="Test Company", plan="pro")
    org = await create_organization(async_session, req, user.id)

    # Verify organization
    assert org.id is not None
    assert org.name == "Test Company"
    assert org.plan == "pro"
    assert org.slug is not None

    # Verify user is owner
    role = await get_user_role_in_org(async_session, user.id, org.id)
    assert role == "owner"


@pytest.mark.asyncio
async def test_create_org_creates_unique_slug(async_session: AsyncSession):
    """Test that unique slugs are generated."""
    user = User(email="user@test.com", password_hash="hash", full_name="User")
    async_session.add(user)
    await async_session.flush()

    req1 = OrganizationCreate(name="Test Org", plan="free")
    org1 = await create_organization(async_session, req1, user.id)

    req2 = OrganizationCreate(name="Test Org", plan="free")
    org2 = await create_organization(async_session, req2, user.id)

    # Slugs should be different
    assert org1.slug != org2.slug


@pytest.mark.asyncio
async def test_get_organization(async_session: AsyncSession):
    """Test retrieving an organization."""
    user = User(email="user@test.com", password_hash="hash", full_name="User")
    async_session.add(user)
    await async_session.flush()

    req = OrganizationCreate(name="Retrieve Test", plan="free")
    org = await create_organization(async_session, req, user.id)

    # Retrieve it
    retrieved = await get_organization(async_session, org.id)
    assert retrieved is not None
    assert retrieved.id == org.id
    assert retrieved.name == "Retrieve Test"


@pytest.mark.asyncio
async def test_get_nonexistent_organization(async_session: AsyncSession):
    """Test retrieving non-existent organization returns None."""
    result = await get_organization(async_session, "nonexistent-id")
    assert result is None


@pytest.mark.asyncio
async def test_update_organization(async_session: AsyncSession):
    """Test updating organization."""
    user = User(email="user@test.com", password_hash="hash", full_name="User")
    async_session.add(user)
    await async_session.flush()

    req = OrganizationCreate(name="Original Name", plan="free")
    org = await create_organization(async_session, req, user.id)

    # Update it
    from app.schemas.organization import OrganizationUpdate

    update_req = OrganizationUpdate(name="Updated Name", plan="pro")
    updated = await update_organization(async_session, org.id, update_req)

    assert updated is not None
    assert updated.name == "Updated Name"
    assert updated.plan == "pro"


@pytest.mark.asyncio
async def test_get_user_role_in_org(async_session: AsyncSession):
    """Test retrieving user's role in organization."""
    user = User(email="user@test.com", password_hash="hash", full_name="User")
    async_session.add(user)
    await async_session.flush()

    req = OrganizationCreate(name="Role Test", plan="free")
    org = await create_organization(async_session, req, user.id)

    # User should be owner
    role = await get_user_role_in_org(async_session, user.id, org.id)
    assert role == "owner"

    # Non-member should return None
    other_user = User(email="other@test.com", password_hash="hash", full_name="Other")
    async_session.add(other_user)
    await async_session.flush()

    role = await get_user_role_in_org(async_session, other_user.id, org.id)
    assert role is None


@pytest.mark.asyncio
async def test_add_member_to_org(async_session: AsyncSession):
    """Test adding a member to organization."""
    owner = User(email="owner@test.com", password_hash="hash", full_name="Owner")
    async_session.add(owner)
    await async_session.flush()

    member = User(email="member@test.com", password_hash="hash", full_name="Member")
    async_session.add(member)
    await async_session.flush()

    req = OrganizationCreate(name="Add Member Test", plan="free")
    org = await create_organization(async_session, req, owner.id)

    # Add member
    membership = await add_member_to_org(async_session, org.id, member.id, role="admin")

    assert membership.organization_id == org.id
    assert membership.user_id == member.id
    assert membership.role == "admin"

    # Verify role
    role = await get_user_role_in_org(async_session, member.id, org.id)
    assert role == "admin"


@pytest.mark.asyncio
async def test_add_duplicate_member(async_session: AsyncSession):
    """Test adding same member twice fails."""
    owner = User(email="owner@test.com", password_hash="hash", full_name="Owner")
    async_session.add(owner)
    await async_session.flush()

    member = User(email="member@test.com", password_hash="hash", full_name="Member")
    async_session.add(member)
    await async_session.flush()

    req = OrganizationCreate(name="Test", plan="free")
    org = await create_organization(async_session, req, owner.id)

    # Add member
    await add_member_to_org(async_session, org.id, member.id, role="viewer")

    # Try to add again
    with pytest.raises(ValueError, match="already member"):
        await add_member_to_org(async_session, org.id, member.id, role="admin")


@pytest.mark.asyncio
async def test_remove_member_from_org(async_session: AsyncSession):
    """Test removing member from organization."""
    owner = User(email="owner@test.com", password_hash="hash", full_name="Owner")
    async_session.add(owner)
    await async_session.flush()

    member = User(email="member@test.com", password_hash="hash", full_name="Member")
    async_session.add(member)
    await async_session.flush()

    req = OrganizationCreate(name="Remove Test", plan="free")
    org = await create_organization(async_session, req, owner.id)

    # Add member
    await add_member_to_org(async_session, org.id, member.id, role="viewer")

    # Verify they're a member
    role = await get_user_role_in_org(async_session, member.id, org.id)
    assert role is not None

    # Remove member
    removed = await remove_member_from_org(async_session, org.id, member.id)
    assert removed is True

    # Verify they're no longer a member
    role = await get_user_role_in_org(async_session, member.id, org.id)
    assert role is None


@pytest.mark.asyncio
async def test_remove_nonexistent_member(async_session: AsyncSession):
    """Test removing non-member returns False."""
    owner = User(email="owner@test.com", password_hash="hash", full_name="Owner")
    async_session.add(owner)
    await async_session.flush()

    req = OrganizationCreate(name="Test", plan="free")
    org = await create_organization(async_session, req, owner.id)

    # Try to remove non-existent member
    removed = await remove_member_from_org(async_session, org.id, "nonexistent-user-id")
    assert removed is False


if __name__ == "__main__":
    print("Run with: pytest apps/api/tests/test_organizations.py -v")
