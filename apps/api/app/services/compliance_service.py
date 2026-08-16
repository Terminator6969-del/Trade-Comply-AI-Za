"""
Compliance service for running deterministic regulatory checks on shipments.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Shipment, LineItem, Document, Party, TariffRecord, AuditLog
from app.rules.engine import compliance_engine, ComplianceReport


async def evaluate_shipment_compliance(
    session: AsyncSession,
    org_id: str,
    shipment_id: str,
    user_id: str | None = None,
) -> ComplianceReport:
    """
    Run the full deterministic compliance rule suite against a shipment.
    Updates the shipment's risk_level and status in the database.
    """
    # 1. Fetch shipment (scoped to tenant)
    result = await session.execute(
        select(Shipment).where(
            Shipment.id == shipment_id,
            Shipment.organization_id == org_id,
        )
    )
    shipment = result.scalar_one_or_none()
    if not shipment:
        raise ValueError(f"Shipment {shipment_id} not found in organization")

    # 2. Fetch line items
    result = await session.execute(
        select(LineItem).where(LineItem.shipment_id == shipment_id)
    )
    line_items = list(result.scalars().all())

    # 3. Fetch documents
    result = await session.execute(
        select(Document).where(Document.shipment_id == shipment_id)
    )
    documents = list(result.scalars().all())

    # 4. Fetch parties
    parties: dict[str, Party] = {}
    if shipment.importer_id:
        r = await session.execute(select(Party).where(Party.id == shipment.importer_id))
        parties["importer"] = r.scalar_one_or_none()
    if shipment.supplier_id:
        r = await session.execute(select(Party).where(Party.id == shipment.supplier_id))
        parties["supplier"] = r.scalar_one_or_none()
    if shipment.clearing_agent_id:
        r = await session.execute(select(Party).where(Party.id == shipment.clearing_agent_id))
        parties["clearing_agent"] = r.scalar_one_or_none()

    # 5. Fetch relevant tariffs
    hs_codes = set()
    for item in line_items:
        if item.hs_code_suggested:
            hs_codes.add(item.hs_code_suggested)

    tariff_map: dict[str, TariffRecord] = {}
    if hs_codes:
        result = await session.execute(
            select(TariffRecord).where(TariffRecord.hs_code.in_(list(hs_codes)))
        )
        for t in result.scalars().all():
            tariff_map[t.hs_code] = t

    # 6. Run compliance engine
    report = compliance_engine.evaluate(
        shipment=shipment,
        line_items=line_items,
        parties=parties,
        documents=documents,
        tariff_map=tariff_map,
    )

    # 7. Update shipment risk_level and status
    shipment.risk_level = report.risk_level
    if not report.is_compliant:
        shipment.status = "needs_review"
    elif shipment.status in ["draft", "needs_review"]:
        shipment.status = "compliance_ready"

    # 8. Record audit log if user_id provided
    if user_id:
        from app.core.audit import log_action
        await log_action(
            session=session,
            organization_id=org_id,
            user_id=user_id,
            action="compliance_check",
            entity_type="shipment",
            entity_id=str(shipment.id),
            after_value={
                "is_compliant": report.is_compliant,
                "risk_level": report.risk_level,
                "passed_count": report.passed_count,
                "warning_count": report.warning_count,
                "error_count": report.error_count,
                "critical_count": report.critical_count,
            },
        )
    await session.commit()

    return report


async def get_shipment_compliance_report(
    session: AsyncSession,
    org_id: str,
    shipment_id: str,
) -> ComplianceReport:
    """Read-only compliance evaluation without mutating shipment status."""
    return await evaluate_shipment_compliance(session, org_id, shipment_id)
