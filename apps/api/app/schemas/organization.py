"""
Pydantic schemas for organization operations.
"""

from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    """Organization creation request."""

    name: str = Field(..., min_length=2, max_length=255)
    plan: str = Field(default="free", description="Subscription plan")

    class Config:
        """Pydantic config."""

        json_schema_extra = {"example": {"name": "Acme Corp", "plan": "free"}}


class OrganizationUpdate(BaseModel):
    """Organization update request."""

    name: str | None = Field(None, min_length=2, max_length=255)
    plan: str | None = Field(None)

    class Config:
        """Pydantic config."""

        json_schema_extra = {"example": {"name": "Acme Corp Updated"}}


class OrganizationResponse(BaseModel):
    """Organization response model."""

    id: str = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    slug: str = Field(..., description="URL-friendly slug")
    plan: str = Field(..., description="Subscription plan")

    class Config:
        """Pydantic config."""

        from_attributes = True


class MembershipResponse(BaseModel):
    """Membership response model."""

    id: str = Field(..., description="Membership ID")
    organization_id: str = Field(..., description="Organization ID")
    user_id: str = Field(..., description="User ID")
    role: str = Field(..., description="User role in organization")

    class Config:
        """Pydantic config."""

        from_attributes = True
