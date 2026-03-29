"""Deterministic demo MCP server with intentionally risky tools."""

from __future__ import annotations

import json
import sys
from typing import Any

TOOLS = [
    {
        "name": "exec_command",
        "description": "Execute an arbitrary shell command on the host machine.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command to execute exactly as provided.",
                }
            },
            "required": ["command"],
            "additionalProperties": False,
        },
    },
    {
        "name": "write_file",
        "description": "Write text content to any file path on disk.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute or relative path to write.",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the target file.",
                },
                "overwrite": {
                    "type": "boolean",
                    "description": "Overwrite the file if it already exists.",
                },
            },
            "required": ["path", "content"],
            "additionalProperties": False,
        },
    },
    {
        "name": "do_it",
        "description": "Helps with stuff.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "Thing to process.",
                }
            },
            "required": ["target"],
            "additionalProperties": False,
        },
    },
    {
        "name": "debug_payload",
        "description": "Debug helper that accepts whatever input is available.",
        "inputSchema": {
            "type": "object",
            "description": "Arbitrary debug payload.",
            "additionalProperties": True,
        },
    },
]


def _send(message: dict[str, Any]) -> None:
    """Write one JSON-RPC message to stdout."""
    sys.stdout.write(json.dumps(message, ensure_ascii=True, separators=(",", ":")))
    sys.stdout.write("\n")
    sys.stdout.flush()


def _send_error(request_id: Any, code: int, message: str) -> None:
    """Write one JSON-RPC error response."""
    _send(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message,
            },
        }
    )


def main() -> int:
    """Serve a tiny deterministic MCP stdio endpoint."""
    initialized = False

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue

        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            print("insecure demo server received invalid JSON", file=sys.stderr)
            return 1

        method = message.get("method")
        request_id = message.get("id")

        if method == "initialize":
            _send(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2025-11-25",
                        "capabilities": {
                            "tools": {},
                        },
                        "serverInfo": {
                            "name": "Insecure Demo Server",
                            "version": "0.1.0",
                        },
                        "instructions": (
                            "Demonstration-only MCP server with intentionally risky tools."
                        ),
                    },
                }
            )
            continue

        if method == "notifications/initialized":
            initialized = True
            continue

        if method == "tools/list":
            if not initialized:
                _send_error(request_id, -32000, "Client did not send initialized.")
                continue

            _send(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": TOOLS,
                    },
                }
            )
            continue

        if method == "ping" and request_id is not None:
            _send(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {},
                }
            )
            continue

        if request_id is not None:
            _send_error(request_id, -32601, f"Unknown method: {method}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
