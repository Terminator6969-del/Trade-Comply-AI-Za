"""
Compliance API routes for running deterministic regulatory checks.
All endpoints are scoped to the authenticated organization.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.dependencies import get_current_user
from app.services.compliance_service import evaluate_shipment_compliance
from app.schemas.compliance import ComplianceReportResponse, ComplianceCheckResponse

router = APIRouter(prefix="/api/v1/compliance", tags=["compliance"])


@router.post("/shipments/{shipment_id}/check", response_model=ComplianceReportResponse)
async def check_compliance(
    shipment_id: str,
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ComplianceReportResponse:
    """
    Run the full deterministic compliance rule suite against a shipment.
    Evaluates SARS documentation, ITAC permits, NRCS LOAs, and Dangerous Goods.
    """
    try:
        report = await evaluate_shipment_compliance(
            session=session,
            org_id=claims["org_id"],
            shipment_id=shipment_id,
            user_id=claims.get("sub"),
        )
        return ComplianceReportResponse(
            shipment_id=report.shipment_id,
            is_compliant=report.is_compliant,
            risk_level=report.risk_level,
            passed_count=report.passed_count,
            warning_count=report.warning_count,
            error_count=report.error_count,
            critical_count=report.critical_count,
            checks=[
                ComplianceCheckResponse(
                    rule_code=c.rule_code,
                    rule_pack=c.rule_pack.value if hasattr(c.rule_pack, "value") else str(c.rule_pack),
                    title=c.title,
                    passed=c.passed,
                    severity=c.severity.value if hasattr(c.severity, "value") else str(c.severity),
                    message=c.message,
                    recommended_action=c.recommended_action,
                    affected_line_items=c.affected_line_items,
                    metadata=c.metadata,
                )
                for c in report.checks
            ],
            summary_notes=report.summary_notes,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/shipments/{shipment_id}", response_model=ComplianceReportResponse)
async def get_compliance(
    shipment_id: str,
    claims: Annotated[dict, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ComplianceReportResponse:
    """
    Retrieve latest compliance evaluation report for a shipment.
    """
    return await check_compliance(shipment_id, claims, session)
