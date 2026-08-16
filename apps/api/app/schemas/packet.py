"""
Pydantic schemas for Customs SAD500 Packet generation.
"""

from typing import Any, Literal
from pydantic import BaseModel, ConfigDict
from app.schemas.duty import DutyEstimateResponse
from app.schemas.compliance import ComplianceReportResponse


class PacketGenerateRequest(BaseModel):
    format: Literal["json", "csv", "summary"] = "json"


class SAD500Header(BaseModel):
    customs_office: str
    declaration_type: str
    declarant_reference: str
    importer_name: str
    importer_customs_code: str | None
    importer_vat: str | None
    supplier_name: str | None
    country_of_origin: str | None
    port_of_entry: str | None
    incoterms: str | None
    currency: str | None


class PacketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    shipment_id: str
    reference: str
    format: str
    sad500_header: SAD500Header
    compliance_report: ComplianceReportResponse
    duty_estimate: DutyEstimateResponse
    raw_content: str | None = None
    created_at: str
