"""
Test suite for database configuration and models.
Tests SQLAlchemy async setup and model registration.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Base, Organization, User, Membership


@pytest.mark.asyncio
async def test_database_connection(async_engine):
    """Test that async database engine can connect."""
    async with async_engine.connect() as conn:
        # If we get here without error, connection works
        assert conn is not None


@pytest.mark.asyncio
async def test_models_registered(async_engine):
    """Test that all models are registered with Base."""
    # Check that models are in Base.metadata.tables
    assert "organizations" in Base.metadata.tables
    assert "users" in Base.metadata.tables
    assert "memberships" in Base.metadata.tables


@pytest.mark.asyncio
async def test_create_organization(async_session: AsyncSession):
    """Test creating an organization."""
    org = Organization(
        name="Test Org",
        slug="test-org",
        plan="free",
    )
    async_session.add(org)
    await async_session.commit()
    await async_session.refresh(org)

    # Verify the organization was created
    assert org.id is not None
    assert org.name == "Test Org"
    assert org.slug == "test-org"
    assert org.plan == "free"


@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession):
    """Test creating a user."""
    user = User(
        email="test@example.com",
        password_hash="hashed_password_here",
        full_name="Test User",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Verify the user was created
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True


@pytest.mark.asyncio
async def test_create_membership(async_session: AsyncSession):
    """Test creating a membership (user-org relationship)."""
    # Create org and user first
    org = Organization(name="Test Org", slug="test-org-2", plan="free")
    async_session.add(org)
    await async_session.flush()

    user = User(
        email="member@example.com",
        password_hash="hashed_password",
        full_name="Member User",
    )
    async_session.add(user)
    await async_session.flush()

    # Create membership
    membership = Membership(
        organization_id=org.id,
        user_id=user.id,
        role="admin",
    )
    async_session.add(membership)
    await async_session.commit()
    await async_session.refresh(membership)

    # Verify membership was created
    assert membership.id is not None
    assert membership.organization_id == org.id
    assert membership.user_id == user.id
    assert membership.role == "admin"


@pytest.mark.asyncio
async def test_query_organization_by_slug(async_session: AsyncSession):
    """Test querying organizations by slug."""
    org = Organization(name="Query Test", slug="query-test", plan="pro")
    async_session.add(org)
    await async_session.commit()

    # Query by slug
    result = await async_session.execute(
        select(Organization).where(Organization.slug == "query-test")
    )
    fetched_org = result.scalar_one_or_none()

    assert fetched_org is not None
    assert fetched_org.name == "Query Test"
    assert fetched_org.plan == "pro"


@pytest.mark.asyncio
async def test_organization_unique_slug(async_session: AsyncSession):
    """Test that organization slug must be unique."""
    org1 = Organization(name="Org 1", slug="unique-slug", plan="free")
    async_session.add(org1)
    await async_session.commit()

    # Try to create another with same slug
    org2 = Organization(name="Org 2", slug="unique-slug", plan="free")
    async_session.add(org2)

    with pytest.raises(Exception):  # IntegrityError
        await async_session.commit()


@pytest.mark.asyncio
async def test_user_unique_email(async_session: AsyncSession):
    """Test that user email must be unique."""
    user1 = User(
        email="unique@example.com",
        password_hash="hash1",
        full_name="User 1",
    )
    async_session.add(user1)
    await async_session.commit()

    # Try to create another with same email
    user2 = User(
        email="unique@example.com",
        password_hash="hash2",
        full_name="User 2",
    )
    async_session.add(user2)

    with pytest.raises(Exception):  # IntegrityError
        await async_session.commit()


if __name__ == "__main__":
    print("Run with: pytest apps/api/tests/test_database.py -v")
