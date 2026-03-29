from __future__ import annotations

from mcp_trust.models import (
    Finding,
    FindingCategory,
    FindingLevel,
    NormalizedServer,
    NormalizedTool,
    Report,
    ScoreBreakdown,
    ScoreCategory,
)
from mcp_trust.reporters import TerminalReporter


def test_terminal_reporter_renders_stable_summary() -> None:
    server = NormalizedServer(
        target='stdio:["python","demo.py"]',
        name="Demo Server",
        version="1.0.0",
        tools=(
            NormalizedTool(
                name="exec_command",
                description="Execute a command.",
                input_schema={
                    "type": "object",
                    "properties": {"command": {"type": "string"}},
                    "required": ["command"],
                    "additionalProperties": False,
                },
            ),
            NormalizedTool(
                name="do_it",
                description="Helps with stuff.",
                input_schema={
                    "type": "object",
                    "properties": {"target": {"type": "string"}},
                    "required": ["target"],
                    "additionalProperties": False,
                },
            ),
        ),
        metadata={"mcp": {"protocolVersion": "2025-11-25"}},
    )
    findings = (
        Finding(
            rule_id="dangerous_exec_tool",
            level=FindingLevel.ERROR,
            title="Dangerous execution tool",
            category=FindingCategory.CAPABILITY,
            score_category=ScoreCategory.TOOL_SURFACE,
            message="Tool 'exec_command' appears to expose host command execution.",
            evidence=("input_keys=['command']",),
            penalty=20,
            tool_name="exec_command",
        ),
        Finding(
            rule_id="vague_tool_description",
            level=FindingLevel.WARNING,
            title="Vague tool description",
            category=FindingCategory.TOOL_DESCRIPTION,
            score_category=ScoreCategory.TOOL_SURFACE,
            message=(
                "Tool 'do_it' uses a vague description that does not "
                "explain its behavior clearly."
            ),
            evidence=("matched_phrase='helps with stuff'",),
            penalty=10,
            tool_name="do_it",
        ),
    )
    report = Report(
        server=server,
        findings=findings,
        score=ScoreBreakdown.from_findings(findings),
    )

    rendered = TerminalReporter().render(report)

    assert rendered.splitlines() == [
        "Server: Demo Server",
        "Version: 1.0.0",
        "Protocol: 2025-11-25",
        'Target: stdio:["python","demo.py"]',
        "Tools: 2",
        "Findings: 2",
        "Severity: error=1, warning=1, info=0",
        "Total Score: 70/100",
        "Category Scores:",
        "- spec: 100/100 (penalties: 0)",
        "- auth: 100/100 (penalties: 0)",
        "- secrets: 100/100 (penalties: 0)",
        "- tool_surface: 70/100 (penalties: 30)",
        "Top Findings:",
        (
            "- ERROR dangerous_exec_tool [exec_command]: Tool 'exec_command' "
            "appears to expose host command execution."
        ),
        (
            "- WARNING vague_tool_description [do_it]: Tool 'do_it' uses a vague "
            "description that does not explain its behavior clearly."
        ),
    ]
