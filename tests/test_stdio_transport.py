from __future__ import annotations

import sys
from pathlib import Path

import pytest

from mcp_trust.transport import ProtocolError, ServerStartupError, TransportTimeoutError
from mcp_trust.transports import StdioServerConfig, StdioTransport

FAKE_SERVER = Path(__file__).resolve().parents[1] / "examples" / "fake_stdio_server.py"


def _fake_server_command(mode: str) -> tuple[str, ...]:
    return (sys.executable, str(FAKE_SERVER), "--mode", mode)


def test_stdio_transport_discovers_and_normalizes_tools() -> None:
    transport = StdioTransport()
    command = _fake_server_command("happy")
    server = transport.scan(
        StdioServerConfig.from_command(command, timeout_seconds=1.0)
    )

    assert server.name == "Fake MCP Server"
    assert server.version == "0.1.0"
    assert server.tool_names == ("add", "echo")
    assert server.tools[0].metadata == {"annotations": {"readOnlyHint": True}}
    assert server.metadata["mcp"] == {
        "protocolVersion": "2025-11-25",
        "capabilities": {"tools": {}},
        "transport": "stdio",
        "command": list(command),
    }


def test_stdio_transport_reports_invalid_tools_payload() -> None:
    transport = StdioTransport()

    with pytest.raises(ProtocolError, match="tools/list result.tools must be a list"):
        transport.scan(
            StdioServerConfig.from_command(
                _fake_server_command("invalid-tools"),
                timeout_seconds=1.0,
            )
        )


def test_stdio_transport_reports_initialize_timeout() -> None:
    transport = StdioTransport()

    with pytest.raises(
        TransportTimeoutError,
        match="Timed out waiting for response to initialize",
    ):
        transport.scan(
            StdioServerConfig.from_command(
                _fake_server_command("slow-init"),
                timeout_seconds=0.2,
            )
        )


def test_stdio_transport_reports_startup_failure() -> None:
    transport = StdioTransport()

    with pytest.raises(ServerStartupError, match="Failed to start stdio server command"):
        transport.scan(
            StdioServerConfig.from_command(
                ("does-not-exist-mcp-server-command",),
                timeout_seconds=1.0,
            )
        )
