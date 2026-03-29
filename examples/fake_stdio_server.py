"""Fake MCP stdio server used for local checks and transport tests."""

from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any

TOOLS = [
    {
        "name": "add",
        "description": "Add two integers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"},
            },
            "required": ["a", "b"],
        },
        "annotations": {"readOnlyHint": True},
    },
    {
        "name": "echo",
        "description": "Return the provided message.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
            },
            "required": ["message"],
        },
    },
]


def _send(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=True, separators=(",", ":")))
    sys.stdout.write("\n")
    sys.stdout.flush()


def _send_error(request_id: Any, code: int, message: str) -> None:
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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("happy", "invalid-tools", "bad-json", "slow-init", "crash"),
        default="happy",
    )
    args = parser.parse_args()

    initialized = False

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue

        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            print("fake server received invalid client JSON", file=sys.stderr)
            return 1

        method = message.get("method")
        request_id = message.get("id")

        if method == "initialize":
            if args.mode == "crash":
                print("fake server crashed before initialize response", file=sys.stderr)
                return 1
            if args.mode == "slow-init":
                time.sleep(1.0)
            if args.mode == "bad-json":
                sys.stdout.write("{not-json}\n")
                sys.stdout.flush()
                continue

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
                            "name": "Fake MCP Server",
                            "version": "0.1.0",
                        },
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
            if args.mode == "invalid-tools":
                _send(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "tools": {
                                "name": "not-a-list",
                            }
                        },
                    }
                )
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
