"""
Base classes and result models for the TradeComply compliance rule engine.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class ComplianceSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class RulePack(str, Enum):
    SARS_VALUATION = "sars_valuation"
    ITAC_PERMITS = "itac_permits"
    NRCS_LOA = "nrcs_loa"
    DANGEROUS_GOODS = "dangerous_goods"
    DOCUMENTATION = "documentation"


@dataclass
class RuleResult:
    """Individual rule evaluation outcome."""
    rule_code: str
    rule_pack: RulePack
    title: str
    passed: bool
    severity: ComplianceSeverity
    message: str
    recommended_action: str | None = None
    affected_line_items: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ComplianceRule(Protocol):
    """Protocol for all deterministic compliance rules."""
    rule_code: str
    rule_pack: RulePack
    title: str

    def evaluate(
        self,
        shipment: Any,
        line_items: list[Any],
        parties: dict[str, Any],
        documents: list[Any],
        tariff_map: dict[str, Any],
    ) -> RuleResult:
        ...
