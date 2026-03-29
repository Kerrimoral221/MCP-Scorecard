"""Shared report summary helpers used by output reporters."""

from __future__ import annotations

from typing import TypedDict

from mcp_trust.models import Finding, FindingLevel, Report

MAX_SUMMARY_FINDINGS = 5


class SummaryFinding(TypedDict):
    """Compact finding representation used by reporters."""

    rule_id: str
    title: str | None
    severity: str
    tool_name: str | None
    message: str
    score_impact: int


class SeverityCounts(TypedDict):
    """Severity counters exposed in the report summary."""

    info: int
    warning: int
    error: int


class ReportSummary(TypedDict):
    """Stable summary view shared by reporters."""

    tool_count: int
    finding_count: int
    severity_counts: SeverityCounts
    top_findings: list[SummaryFinding]


def build_report_summary(report: Report) -> ReportSummary:
    """Build a stable summary view from an already computed report."""
    severity_counts: SeverityCounts = {
        "info": sum(1 for finding in report.findings if finding.severity is FindingLevel.INFO),
        "warning": sum(
            1 for finding in report.findings if finding.severity is FindingLevel.WARNING
        ),
        "error": sum(1 for finding in report.findings if finding.severity is FindingLevel.ERROR),
    }
    top_findings = [
        _serialize_summary_finding(finding)
        for finding in report.findings[:MAX_SUMMARY_FINDINGS]
    ]

    return {
        "tool_count": len(report.server.tools),
        "finding_count": report.finding_count,
        "severity_counts": severity_counts,
        "top_findings": top_findings,
    }


def _serialize_summary_finding(finding: Finding) -> SummaryFinding:
    """Return a short, stable summary representation of one finding."""
    return {
        "rule_id": finding.rule_id,
        "title": finding.title,
        "severity": finding.severity.value,
        "tool_name": finding.tool_name,
        "message": finding.message,
        "score_impact": finding.score_impact,
    }
