"""
Customs SAD500 Packet Generation Service.
Generates customs declaration packets in JSON, CSV (for CargoWise / SoftClear / EasyClear import), and text summary formats.
"""

import csv
import io
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Shipment, LineItem, Party, AuditLog
from app.services.compliance_service import evaluate_shipment_compliance
from app.services.duty_service import calculate_shipment_duties
from app.schemas.packet import PacketResponse, SAD500Header
from app.schemas.compliance import ComplianceReportResponse, ComplianceCheckResponse


async def generate_customs_packet(
    session: AsyncSession,
    org_id: str,
    shipment_id: str,
    output_format: str = "json",
    user_id: str | None = None,
) -> PacketResponse:
    """
    Generate a full Customs SAD500 packet containing declaration headers, line items,
    duty & VAT math, and compliance check audit.
    """
    # 1. Fetch shipment
    result = await session.execute(
        select(Shipment).where(
            Shipment.id == shipment_id,
            Shipment.organization_id == org_id,
        )
    )
    shipment = result.scalar_one_or_none()
    if not shipment:
        raise ValueError(f"Shipment {shipment_id} not found in organization")

    # 2. Fetch parties
    importer: Party | None = None
    supplier: Party | None = None
    if shipment.importer_id:
        r = await session.execute(select(Party).where(Party.id == shipment.importer_id))
        importer = r.scalar_one_or_none()
    if shipment.supplier_id:
        r = await session.execute(select(Party).where(Party.id == shipment.supplier_id))
        supplier = r.scalar_one_or_none()

    # 3. Calculate duties
    duty_est = await calculate_shipment_duties(session, org_id, shipment_id)

    # 4. Evaluate compliance
    comp_rep = await evaluate_shipment_compliance(session, org_id, shipment_id, user_id=user_id)

    # 5. Build SAD500 header
    header = SAD500Header(
        customs_office="ZA - Durban Harbour (002)" if (shipment.port_of_discharge or "").lower() == "durban" else "ZA - SARS Customs",
        declaration_type=f"SAD500 / {shipment.shipment_type.upper()}",
        declarant_reference=shipment.reference,
        importer_name=importer.name if importer else "Undeclared Importer",
        importer_customs_code=getattr(importer, "customs_code", None),
        importer_vat=getattr(importer, "vat_number", None),
        supplier_name=supplier.name if supplier else "Overseas Supplier",
        country_of_origin=shipment.origin_country,
        port_of_entry=shipment.port_of_discharge or "DURBAN",
        incoterms=shipment.incoterms,
        currency=shipment.currency,
    )

    # 6. Format raw content based on requested format
    raw_content = None
    if output_format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "ItemNo",
            "Description",
            "HSCode",
            "Quantity",
            "Currency",
            "ForeignValue",
            "CustomsValueZAR",
            "DutyRatePct",
            "DutyZAR",
            "ATVZAR",
            "VATRatePct",
            "VATZAR",
            "TotalTaxZAR",
        ])
        for idx, item in enumerate(duty_est.line_items, 1):
            writer.writerow([
                idx,
                item.description,
                item.hs_code or "",
                item.quantity,
                item.currency,
                item.foreign_total_value,
                item.customs_value_zar,
                item.duty_rate_percent,
                item.duty_amount_zar,
                item.atv_zar,
                item.vat_rate_percent,
                item.vat_amount_zar,
                item.total_tax_zar,
            ])
        writer.writerow([])
        writer.writerow(["TOTALS", "", "", "", "", duty_est.total_customs_value_foreign, duty_est.total_customs_value_zar, "", duty_est.total_customs_duty_zar, duty_est.total_atv_zar, "", duty_est.total_import_vat_zar, duty_est.total_payable_to_sars_zar])
        raw_content = output.getvalue()

    elif output_format == "summary":
        lines = [
            f"=== SARS SAD500 CUSTOMS DECLARATION PACKET ===",
            f"Reference: {shipment.reference}",
            f"Declaration Type: {header.declaration_type}",
            f"Customs Office: {header.customs_office}",
            f"Importer: {header.importer_name} (Customs Code: {header.importer_customs_code or 'N/A'}, VAT: {header.importer_vat or 'N/A'})",
            f"Supplier: {header.supplier_name} (Origin: {header.country_of_origin or 'N/A'})",
            f"Port of Entry: {header.port_of_entry} | Incoterms: {header.incoterms or 'N/A'} | Currency: {header.currency or 'N/A'}",
            f"Exchange Rate: 1 {duty_est.currency} = R {duty_est.exchange_rate_to_zar:.2f}",
            "",
            f"--- FINANCIAL SUMMARY (ZAR) ---",
            f"Customs Value:        R {duty_est.total_customs_value_zar:,.2f}",
            f"Customs Duty:         R {duty_est.total_customs_duty_zar:,.2f}",
            f"SARS Added Tax Value: R {duty_est.total_atv_zar:,.2f}",
            f"Import VAT (15%):     R {duty_est.total_import_vat_zar:,.2f}",
            f"TOTAL PAYABLE TO SARS: R {duty_est.total_payable_to_sars_zar:,.2f}",
            "",
            f"--- COMPLIANCE STATUS ---",
            f"Risk Level: {comp_rep.risk_level.upper()} | Passed: {comp_rep.passed_count} | Warnings: {comp_rep.warning_count} | Errors: {comp_rep.error_count} | Critical: {comp_rep.critical_count}",
        ]
        if comp_rep.summary_notes:
            lines.append("Flags:")
            for note in comp_rep.summary_notes:
                lines.append(f"  {note}")
        raw_content = "\n".join(lines)

    # 7. Update shipment status to packet_generated if compliant
    if comp_rep.is_compliant:
        shipment.status = "packet_generated"
    await session.commit()

    # 8. Record audit log if user_id provided
    if user_id:
        from app.core.audit import log_action
        await log_action(
            session=session,
            organization_id=org_id,
            user_id=user_id,
            action="generate_packet",
            entity_type="shipment",
            entity_id=str(shipment.id),
            after_value={
                "format": output_format,
                "total_payable_zar": duty_est.total_payable_to_sars_zar,
                "risk_level": comp_rep.risk_level,
            },
        )
    await session.commit()

    # Transform report for Pydantic response
    compliance_response = ComplianceReportResponse(
        shipment_id=comp_rep.shipment_id,
        is_compliant=comp_rep.is_compliant,
        risk_level=comp_rep.risk_level,
        passed_count=comp_rep.passed_count,
        warning_count=comp_rep.warning_count,
        error_count=comp_rep.error_count,
        critical_count=comp_rep.critical_count,
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
            for c in comp_rep.checks
        ],
        summary_notes=comp_rep.summary_notes,
    )

    return PacketResponse(
        shipment_id=str(shipment.id),
        reference=shipment.reference,
        format=output_format,
        sad500_header=header,
        compliance_report=compliance_response,
        duty_estimate=duty_est,
        raw_content=raw_content,
        created_at=datetime.utcnow().isoformat(),
    )
