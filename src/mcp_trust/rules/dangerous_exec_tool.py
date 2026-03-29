"""Rule for shell or command execution style tools."""

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

_NAME_MARKERS = ("exec", "shell", "command", "cmd", "bash", "powershell", "terminal")
_DESCRIPTION_MARKERS = ("execute", "shell command", "host machine", "arbitrary command")
_INPUT_KEYS = ("command", "cmd", "script", "shell")


@dataclass(slots=True, frozen=True)
class DangerousExecToolRule(Rule):
    """Flag tools that appear to execute host commands."""

    rule_id: str = "dangerous_exec_tool"
    title: str = "Dangerous execution tool"
    summary: str = "Tools that execute host shell commands are high risk."
    severity: FindingLevel = FindingLevel.ERROR
    category: FindingCategory = FindingCategory.CAPABILITY
    score_category: ScoreCategory = ScoreCategory.TOOL_SURFACE
    tags: tuple[str, ...] = ("capability", "execution")

    def evaluate(self, server: NormalizedServer) -> tuple[Finding, ...]:
        """Return findings for tools that match the exec heuristic."""
        findings: list[Finding] = []

        for tool in server.tools:
            evidence = self._collect_evidence(
                tool.name,
                tool.description,
                tool.input_schema,
            )
            if not evidence:
                continue

            findings.append(
                self.make_finding(
                    f"Tool {tool.name!r} appears to expose host command execution.",
                    tool_name=tool.name,
                    evidence=evidence,
                )
            )

        return tuple(findings)

    def _collect_evidence(
        self,
        name: str,
        description: str | None,
        input_schema: dict[str, JSONValue],
    ) -> tuple[str, ...]:
        """Return stable evidence for tools that look like exec primitives."""
        normalized_name = name.lower()
        normalized_description = "" if description is None else description.lower()
        property_names = tuple(self._schema_property_names(input_schema))

        matched_name_markers = tuple(
            marker for marker in _NAME_MARKERS if marker in normalized_name
        )
        matched_description_markers = tuple(
            marker for marker in _DESCRIPTION_MARKERS if marker in normalized_description
        )
        matched_input_keys = tuple(key for key in _INPUT_KEYS if key in property_names)

        if not matched_name_markers:
            return ()
        if not matched_description_markers and not matched_input_keys:
            return ()

        evidence = [f"name_markers={list(matched_name_markers)!r}"]
        if matched_description_markers:
            evidence.append(f"description_markers={list(matched_description_markers)!r}")
        if matched_input_keys:
            evidence.append(f"input_keys={list(matched_input_keys)!r}")
        return tuple(evidence)

    def _schema_property_names(self, input_schema: dict[str, JSONValue]) -> tuple[str, ...]:
        """Return schema property names when available."""
        properties = input_schema.get("properties")
        if not isinstance(properties, dict):
            return ()
        return tuple(
            key.lower()
            for key in properties
            if isinstance(key, str)
        )
