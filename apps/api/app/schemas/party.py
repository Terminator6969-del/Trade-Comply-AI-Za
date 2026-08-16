"""
Pydantic schemas for Party operations.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID


class PartyCreate(BaseModel):
    """Party creation request."""

    party_type: str = Field(
        ..., 
        description="Type of party: importer, exporter, supplier, consignee, clearing_agent, transporter, notify_party"
    )
    name: str = Field(..., min_length=2, max_length=255)
    registration_number: Optional[str] = Field(None, max_length=100)
    vat_number: Optional[str] = Field(None, max_length=50)
    customs_code: Optional[str] = Field(None, max_length=50)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=2, pattern="^[A-Z]{2}$")
    contact_person: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "party_type": "importer",
                "name": "Cape Town Energy Supplies",
                "vat_number": "4123456789",
                "customs_code": "1234567",
                "address_line1": "123 Commissioner Street",
                "city": "Cape Town",
                "postal_code": "8001",
                "country": "ZA",
                "contact_person": "John Smith",
                "email": "john@ctenergy.co.za",
                "phone": "+27 21 555 0123"
            }
        }


class PartyUpdate(BaseModel):
    """Party update request."""

    party_type: Optional[str] = None
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    registration_number: Optional[str] = Field(None, max_length=100)
    vat_number: Optional[str] = Field(None, max_length=50)
    customs_code: Optional[str] = Field(None, max_length=50)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=2, pattern="^[A-Z]{2}$")
    contact_person: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cape Town Energy Supplies (Pty) Ltd",
                "contact_person": "Jane Smith"
            }
        }


class PartyResponse(BaseModel):
    """Party response model."""

    id: str
    organization_id: str
    party_type: str
    name: str
    registration_number: Optional[str]
    vat_number: Optional[str]
    customs_code: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    contact_person: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class PartyListResponse(BaseModel):
    """Paginated party list response."""

    items: list
    total: int
    page: int
    per_page: int
    total_pages: int
