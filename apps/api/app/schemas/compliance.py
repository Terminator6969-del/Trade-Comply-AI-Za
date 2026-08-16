"""
Pydantic schemas for compliance check results and reports.
"""

from typing import Any
from pydantic import BaseModel, ConfigDict


class ComplianceCheckResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rule_code: str
    rule_pack: str
    title: str
    passed: bool
    severity: str
    message: str
    recommended_action: str | None = None
    affected_line_items: list[str] = []
    metadata: dict[str, Any] = {}


class ComplianceReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    shipment_id: str
    is_compliant: bool
    risk_level: str
    passed_count: int
    warning_count: int
    error_count: int
    critical_count: int
    checks: list[ComplianceCheckResponse]
    summary_notes: list[str]
