"""
Organization service for managing organizations and memberships.
"""

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, Membership, User
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


async def get_organization(
    session: AsyncSession,
    org_id: str,
) -> Organization | None:
    """Get organization by ID."""
    result = await session.execute(select(Organization).where(Organization.id == org_id))
    return result.scalar_one_or_none()


async def get_organization_by_slug(
    session: AsyncSession,
    slug: str,
) -> Organization | None:
    """Get organization by slug."""
    result = await session.execute(select(Organization).where(Organization.slug == slug))
    return result.scalar_one_or_none()


async def create_organization(
    session: AsyncSession,
    request: OrganizationCreate,
    user_id: str,
) -> Organization:
    """
    Create a new organization and add user as owner.
    
    Args:
        session: Database session
        request: Organization creation request
        user_id: ID of user creating org (will be owner)
        
    Returns:
        Created Organization
        
    Raises:
        ValueError: If slug already exists
    """
    # Generate unique slug
    slug = f"{request.name.lower().replace(' ', '-')}-{str(uuid4())[:8]}"

    # Check slug doesn't exist
    result = await session.execute(select(Organization).where(Organization.slug == slug))
    if result.scalar_one_or_none():
        raise ValueError(f"Organization slug {slug} already exists")

    organization = Organization(
        name=request.name,
        slug=slug,
        plan=request.plan,
    )
    session.add(organization)
    await session.flush()

    # Add user as owner
    membership = Membership(
        organization_id=organization.id,
        user_id=user_id,
        role="owner",
    )
    session.add(membership)
    await session.commit()

    return organization


async def update_organization(
    session: AsyncSession,
    org_id: str,
    request: OrganizationUpdate,
) -> Organization | None:
    """
    Update organization details.
    
    Args:
        session: Database session
        org_id: Organization ID
        request: Update request
        
    Returns:
        Updated Organization or None if not found
    """
    org = await get_organization(session, org_id)
    if not org:
        return None

    if request.name is not None:
        org.name = request.name

    if request.plan is not None:
        org.plan = request.plan

    await session.commit()
    return org


async def get_user_role_in_org(
    session: AsyncSession,
    user_id: str,
    org_id: str,
) -> str | None:
    """
    Get user's role in an organization.
    
    Returns:
        Role string or None if user not member
    """
    result = await session.execute(
        select(Membership).where(
            Membership.user_id == user_id,
            Membership.organization_id == org_id,
        )
    )
    membership = result.scalar_one_or_none()
    return membership.role if membership else None


async def add_member_to_org(
    session: AsyncSession,
    org_id: str,
    user_id: str,
    role: str = "viewer",
) -> Membership:
    """
    Add a user to an organization with specified role.
    
    Args:
        session: Database session
        org_id: Organization ID
        user_id: User ID to add
        role: Role to assign (default: viewer)
        
    Returns:
        Created Membership
        
    Raises:
        ValueError: If user already member or user/org doesn't exist
    """
    # Check org exists
    org = await get_organization(session, org_id)
    if not org:
        raise ValueError(f"Organization {org_id} not found")

    # Check user exists
    result = await session.execute(select(User).where(User.id == user_id))
    if not result.scalar_one_or_none():
        raise ValueError(f"User {user_id} not found")

    # Check user not already member
    existing = await session.execute(
        select(Membership).where(
            Membership.user_id == user_id,
            Membership.organization_id == org_id,
        )
    )
    if existing.scalar_one_or_none():
        raise ValueError(f"User {user_id} already member of org {org_id}")

    membership = Membership(
        organization_id=org_id,
        user_id=user_id,
        role=role,
    )
    session.add(membership)
    await session.commit()

    return membership


async def remove_member_from_org(
    session: AsyncSession,
    org_id: str,
    user_id: str,
) -> bool:
    """
    Remove a user from an organization.
    
    Args:
        session: Database session
        org_id: Organization ID
        user_id: User ID to remove
        
    Returns:
        True if removed, False if membership not found
    """
    result = await session.execute(
        select(Membership).where(
            Membership.user_id == user_id,
            Membership.organization_id == org_id,
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        return False

    await session.delete(membership)
    await session.commit()

    return True
