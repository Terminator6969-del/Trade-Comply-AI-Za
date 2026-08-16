"""
Pydantic schemas for shipment management.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ShipmentBase(BaseModel):
    """Base shipment schema with common fields."""

    reference: str = Field(..., min_length=3, max_length=100, description="Shipment reference number")
    shipment_type: str = Field(
        default="import",
        description="Shipment type",
        pattern="^(import|export|transit)$",
    )
    transport_mode: Optional[str] = Field(None, pattern="^(sea|air|road|rail)$")
    origin_country: Optional[str] = Field(None, pattern="^[A-Z]{2}$")
    destination_country: Optional[str] = Field(None, pattern="^[A-Z]{2}$")
    port_of_loading: Optional[str] = Field(None, max_length=100)
    port_of_discharge: Optional[str] = Field(None, max_length=100)
    border_post: Optional[str] = Field(None, max_length=100)
    incoterms: Optional[str] = Field(None, max_length=10)
    currency: Optional[str] = Field(None, pattern="^[A-Z]{3}$")
    invoice_date: Optional[date] = None
    estimated_arrival_date: Optional[date] = None
    importer_id: Optional[str] = None
    exporter_id: Optional[str] = None
    supplier_id: Optional[str] = None
    consignee_id: Optional[str] = None
    notify_party_id: Optional[str] = None
    clearing_agent_id: Optional[str] = None


class ShipmentCreate(ShipmentBase):
    """Shipment creation request."""

    reference: str = Field(..., min_length=3, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "reference": "IMP-2026-001",
                "shipment_type": "import",
                "transport_mode": "sea",
                "origin_country": "CN",
                "destination_country": "ZA",
                "port_of_loading": "Shanghai",
                "port_of_discharge": "Durban",
                "incoterms": "FOB",
                "currency": "USD",
                "importer_id": "party-uuid-1",
                "exporter_id": "party-uuid-2",
                "supplier_id": "party-uuid-3",
            }
        }


class ShipmentUpdate(BaseModel):
    """Shipment update request."""

    reference: Optional[str] = Field(None, min_length=3, max_length=100)
    shipment_type: Optional[str] = Field(None, pattern="^(import|export|transit)$")
    transport_mode: Optional[str] = Field(None, pattern="^(sea|air|road|rail)$")
    status: Optional[str] = Field(None, pattern="^(draft|documents_received|extracting|needs_review|compliance_ready|approved|packet_generated|completed|rejected|archived)$")
    risk_level: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    origin_country: Optional[str] = Field(None, pattern="^[A-Z]{2}$")
    destination_country: Optional[str] = Field(None, pattern="^[A-Z]{2}$")
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None
    border_post: Optional[str] = None
    incoterms: Optional[str] = None
    currency: Optional[str] = Field(None, pattern="^[A-Z]{3}$")
    invoice_date: Optional[date] = None
    estimated_arrival_date: Optional[date] = None
    importer_id: Optional[str] = None
    exporter_id: Optional[str] = None
    supplier_id: Optional[str] = None
    consignee_id: Optional[str] = None
    notify_party_id: Optional[str] = None
    clearing_agent_id: Optional[str] = None


class ShipmentResponse(ShipmentBase):
    """Shipment response model."""

    id: str
    organization_id: str
    status: str
    risk_level: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ShipmentListResponse(BaseModel):
    """Paginated shipment list response."""

    items: list
    total: int
    page: int
    per_page: int
    total_pages: int
