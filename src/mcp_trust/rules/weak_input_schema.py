"""Rule for overly weak tool input schemas."""

from __future__ import annotations

from dataclasses import dataclass

from mcp_trust.models import (
    Finding,
    FindingCategory,
    FindingLevel,
    JSONValue,
    NormalizedServer,
    ScoreCategory,
)
from mcp_trust.rules.base import Rule


@dataclass(slots=True, frozen=True)
class WeakInputSchemaRule(Rule):
    """Flag schemas that accept unconstrained arbitrary payloads."""

    rule_id: str = "weak_input_schema"
    title: str = "Weak input schema"
    summary: str = "Tool input schemas should constrain accepted input clearly."
    severity: FindingLevel = FindingLevel.WARNING
    category: FindingCategory = FindingCategory.INPUT_SCHEMA
    score_category: ScoreCategory = ScoreCategory.TOOL_SURFACE
    tags: tuple[str, ...] = ("schema", "validation")

    def evaluate(self, server: NormalizedServer) -> tuple[Finding, ...]:
        """Return findings for tools with weak or open-ended schemas."""
        findings: list[Finding] = []

        for tool in server.tools:
            reasons = self._collect_reasons(tool.input_schema)
            if not reasons:
                continue

            findings.append(
                self.make_finding(
                    (
                        f"Tool {tool.name!r} exposes a weak input schema that accepts "
                        "poorly constrained input."
                    ),
                    tool_name=tool.name,
                    evidence=tuple(reasons),
                )
            )

        return tuple(findings)

    def _collect_reasons(self, input_schema: dict[str, JSONValue]) -> tuple[str, ...]:
        """Return stable evidence lines when the schema is too permissive."""
        reasons: list[str] = []

        schema_type = input_schema.get("type")
        if schema_type != "object":
            reasons.append(f"schema_type={schema_type!r}")
            return tuple(reasons)

        properties = input_schema.get("properties")
        additional_properties = input_schema.get("additionalProperties")

        if additional_properties is True:
            reasons.append("additionalProperties=True")

        if not isinstance(properties, dict) or not properties:
            if additional_properties is not False:
                reasons.append("properties=<missing-or-empty>")

        return tuple(reasons)
