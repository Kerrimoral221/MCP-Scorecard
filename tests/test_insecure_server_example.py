from __future__ import annotations

import sys
from pathlib import Path

from mcp_trust.transports import StdioServerConfig, StdioTransport

INSECURE_SERVER = (
    Path(__file__).resolve().parents[1] / "examples" / "insecure-server" / "server.py"
)


def test_insecure_server_example_exposes_stable_risky_tool_surface() -> None:
    transport = StdioTransport()
    command = (sys.executable, str(INSECURE_SERVER))

    server = transport.scan(
        StdioServerConfig.from_command(command, timeout_seconds=1.0)
    )

    assert server.name == "Insecure Demo Server"
    assert server.version == "0.1.0"
    assert server.tool_names == (
        "exec_command",
        "write_file",
        "do_it",
        "debug_payload",
    )

    tools_by_name = {tool.name: tool for tool in server.tools}

    assert tools_by_name["exec_command"].description == (
        "Execute an arbitrary shell command on the host machine."
    )
    assert tools_by_name["write_file"].description == (
        "Write text content to any file path on disk."
    )
    assert tools_by_name["do_it"].description == "Helps with stuff."
    assert tools_by_name["debug_payload"].input_schema == {
        "type": "object",
        "description": "Arbitrary debug payload.",
        "additionalProperties": True,
    }
