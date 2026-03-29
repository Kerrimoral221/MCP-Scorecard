"""Terminal summary formatting for reports."""

from __future__ import annotations

from mcp_trust.models import Finding, Report, ScoreCategory
from mcp_trust.reporters.summary import build_report_summary


class TerminalReporter:
    """Render a concise terminal summary for a computed report."""

    reporter_id = "terminal"
    default_filename = "mcp-trust-summary.txt"

    def render(self, report: Report) -> str:
        """Render the report as plain text for terminal output."""
        summary = build_report_summary(report)
        severity_counts = summary["severity_counts"]
        protocol_version = _protocol_version(report)

        lines = [
            f"Server: {report.server.name or '<unknown>'}",
            f"Version: {report.server.version or '<unknown>'}",
            f"Target: {report.server.target}",
            f"Tools: {summary['tool_count']}",
            f"Findings: {summary['finding_count']}",
            (
                "Severity: "
                f"error={severity_counts['error']}, "
                f"warning={severity_counts['warning']}, "
                f"info={severity_counts['info']}"
            ),
            f"Total Score: {report.total_score}/{report.score.max_score}",
            "Category Scores:",
        ]
        if protocol_version is not None:
            lines.insert(2, f"Protocol: {protocol_version}")

        for category in ScoreCategory:
            category_score = report.score.category_breakdown[category]
            lines.append(
                f"- {category.value}: {category_score.score}/{category_score.max_score} "
                f"(penalties: {category_score.penalty_points})"
            )

        lines.append("Top Findings:")
        if not report.findings:
            lines.append("- none")
        else:
            for finding in report.findings[:5]:
                lines.append(_format_finding_line(finding))

        return "\n".join(lines) + "\n"


def _format_finding_line(finding: Finding) -> str:
    """Return one concise terminal line for a finding."""
    tool_suffix = "" if finding.tool_name is None else f" [{finding.tool_name}]"
    return (
        f"- {finding.severity.value.upper()} {finding.rule_id}{tool_suffix}: "
        f"{finding.message}"
    )


def _protocol_version(report: Report) -> str | None:
    """Return protocol version from normalized server metadata when present."""
    mcp_metadata = report.server.metadata.get("mcp")
    if not isinstance(mcp_metadata, dict):
        return None
    protocol_version = mcp_metadata.get("protocolVersion")
    if not isinstance(protocol_version, str):
        return None
    return protocol_version
