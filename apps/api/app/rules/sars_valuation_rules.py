"""
SARS Valuation and Mandatory Documentation rules for South African Customs.
"""

from typing import Any
from app.rules.base import ComplianceSeverity, RulePack, RuleResult


class MissingCommercialInvoiceRule:
    """Checks whether at least one Commercial Invoice document is uploaded."""
    rule_code = "SARS-DOC-001"
    rule_pack = RulePack.DOCUMENTATION
    title = "Commercial Invoice Requirement"

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        has_invoice = any(
            d.document_type in ["invoice", "commercial_invoice"]
            for d in documents
        )
        if not has_invoice:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.CRITICAL,
                message="Missing commercial invoice. SARS SAD500 clearance strictly requires a valid supplier invoice.",
                recommended_action="Upload the commercial invoice PDF before submitting clearance draft.",
            )
        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message="Commercial invoice is present.",
        )


class MissingVatOrCustomsCodeRule:
    """Verifies that the South African importer has a registered Customs Code and VAT number."""
    rule_code = "SARS-VAL-002"
    rule_pack = RulePack.SARS_VALUATION
    title = "Importer Customs & VAT Registration"

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        importer = parties.get("importer")
        if not importer:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.ERROR,
                message="No Importer party assigned to this shipment.",
                recommended_action="Assign a registered South African importer entity to the shipment.",
            )

        missing_fields = []
        if not getattr(importer, "customs_code", None):
            missing_fields.append("SARS Customs Code (CCN)")
        if not getattr(importer, "vat_number", None):
            missing_fields.append("VAT Number")

        if missing_fields:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.WARNING,
                message=f"Importer '{importer.name}' is missing: {', '.join(missing_fields)}.",
                recommended_action="Update the importer profile with their valid SARS Customs Code and VAT registration number.",
            )

        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message=f"Importer '{importer.name}' has valid Customs Code ({importer.customs_code}) and VAT registration.",
        )


class IncotermsCurrencyValidationRule:
    """Validates that Incoterms and Invoice Currency are declared."""
    rule_code = "SARS-VAL-003"
    rule_pack = RulePack.SARS_VALUATION
    title = "Incoterms and Currency Declaration"

    VALID_INCOTERMS = {"FOB", "CIF", "CFR", "EXW", "DDP", "DAP", "CPT", "CIP", "FCA", "FAS"}
    VALID_CURRENCIES = {"ZAR", "USD", "EUR", "GBP", "CNY", "JPY", "INR", "AUD", "CAD"}

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        incoterms = getattr(shipment, "incoterms", None)
        currency = getattr(shipment, "currency", None)

        issues = []
        if not incoterms or incoterms.upper() not in self.VALID_INCOTERMS:
            issues.append(f"Incoterm '{incoterms}' is missing or invalid")
        if not currency or currency.upper() not in self.VALID_CURRENCIES:
            issues.append(f"Currency '{currency}' is missing or unrecognised")

        if issues:
            return RuleResult(
                rule_code=self.rule_code,
                rule_pack=self.rule_pack,
                title=self.title,
                passed=False,
                severity=ComplianceSeverity.ERROR,
                message=f"Valuation header issue: {'; '.join(issues)}.",
                recommended_action="Specify valid Incoterms (e.g. FOB, CIF) and standard 3-letter ISO currency (e.g. USD, EUR, ZAR).",
            )

        return RuleResult(
            rule_code=self.rule_code,
            rule_pack=self.rule_pack,
            title=self.title,
            passed=True,
            severity=ComplianceSeverity.INFO,
            message=f"Declared Incoterms: {incoterms}, Currency: {currency}.",
        )
