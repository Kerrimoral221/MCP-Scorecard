# Insecure Demo Server

This example is a tiny deterministic MCP server that intentionally exposes risky tools.

It exists for:

- local manual checks with `mcp-trust scan`
- future README screenshots and examples
- stable scanner tests that should always produce the same findings

## Why It Is Insecure

The tool surface is intentionally problematic:

- `exec_command`: arbitrary shell execution
- `write_file`: filesystem write access
- `do_it`: vague, low-quality description
- `debug_payload`: excessively weak input schema with open-ended arbitrary payload

## Run Locally

From the repository root:

```powershell
python examples\insecure-server\server.py
```

Scan it with MCP Trust Kit:

```powershell
mcp-trust scan --cmd python examples\insecure-server\server.py
```

Or, if using the local virtual environment:

```powershell
.\.venv\Scripts\mcp-trust scan --cmd .\.venv\Scripts\python examples\insecure-server\server.py
```

Sample launch artifacts generated from this server:

- [`sample-reports/insecure-server.report.json`](../../sample-reports/insecure-server.report.json)
- [`sample-reports/insecure-server.report.sarif`](../../sample-reports/insecure-server.report.sarif)
- [`sample-reports/insecure-server.terminal.md`](../../sample-reports/insecure-server.terminal.md)

## Expected Findings

This example should reliably trigger findings such as:

- dangerous shell execution capability
- filesystem write capability
- vague or low-signal tool description
- overly permissive input schema

## Notes

- This server is intentionally insecure and should not be used outside demos/tests.
- It implements only the minimal MCP handshake needed for local discovery.
