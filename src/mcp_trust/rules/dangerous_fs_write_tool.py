"""Rule for filesystem write style tools."""

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

_WRITE_MARKERS = ("write", "save", "append", "create", "update", "edit")
_FILE_MARKERS = ("file", "filesystem", "disk", "path")
_PATH_KEYS = ("path", "file_path", "filepath", "filename", "target_path")
_CONTENT_KEYS = ("content", "text", "body", "data", "contents")


@dataclass(slots=True, frozen=True)
class DangerousFsWriteToolRule(Rule):
    """Flag tools that appear to modify files on disk."""

    rule_id: str = "dangerous_fs_write_tool"
    title: str = "Dangerous filesystem write tool"
    summary: str = "Tools that write files on disk are high risk."
    severity: FindingLevel = FindingLevel.ERROR
    category: FindingCategory = FindingCategory.CAPABILITY
    score_category: ScoreCategory = ScoreCategory.TOOL_SURFACE
    tags: tuple[str, ...] = ("capability", "filesystem")

    def evaluate(self, server: NormalizedServer) -> tuple[Finding, ...]:
        """Return findings for tools that match the fs write heuristic."""
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
                    f"Tool {tool.name!r} appears to provide filesystem write access.",
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
        """Return stable evidence for tools that look like file writers."""
        normalized_name = name.lower()
        normalized_description = "" if description is None else description.lower()
        property_names = tuple(self._schema_property_names(input_schema))

        matched_write_markers = tuple(
            marker for marker in _WRITE_MARKERS if marker in normalized_name
        )
        matched_file_markers = tuple(
            marker
            for marker in _FILE_MARKERS
            if marker in normalized_name or marker in normalized_description
        )
        matched_path_keys = tuple(key for key in _PATH_KEYS if key in property_names)
        matched_content_keys = tuple(key for key in _CONTENT_KEYS if key in property_names)

        if not matched_write_markers:
            return ()
        if not matched_file_markers:
            return ()
        if not matched_path_keys:
            return ()

        evidence = [
            f"write_markers={list(matched_write_markers)!r}",
            f"file_markers={list(matched_file_markers)!r}",
            f"path_keys={list(matched_path_keys)!r}",
        ]
        if matched_content_keys:
            evidence.append(f"content_keys={list(matched_content_keys)!r}")
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
