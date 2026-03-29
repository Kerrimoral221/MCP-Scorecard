"""Default deterministic ruleset for MCP Trust Kit v0."""

from __future__ import annotations

from mcp_trust.rules.dangerous_exec_tool import DangerousExecToolRule
from mcp_trust.rules.dangerous_fs_write_tool import DangerousFsWriteToolRule
from mcp_trust.rules.duplicate_tool_names import DuplicateToolNamesRule
from mcp_trust.rules.missing_tool_description import MissingToolDescriptionRule
from mcp_trust.rules.registry import RuleRegistry
from mcp_trust.rules.vague_tool_description import VagueToolDescriptionRule
from mcp_trust.rules.weak_input_schema import WeakInputSchemaRule

RULES_V0 = (
    DuplicateToolNamesRule(),
    MissingToolDescriptionRule(),
    VagueToolDescriptionRule(),
    WeakInputSchemaRule(),
    DangerousExecToolRule(),
    DangerousFsWriteToolRule(),
)


def build_v0_rule_registry() -> RuleRegistry:
    """Return the default ordered ruleset for MCP Trust Kit v0."""
    return RuleRegistry.from_rules(RULES_V0)
