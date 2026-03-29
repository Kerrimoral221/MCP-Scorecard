# MCP Trust Kit

[![Build Status](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/<owner>/<repo>?sort=semver)](https://github.com/<owner>/<repo>/releases)
[![License](https://img.shields.io/github/license/<owner>/<repo>)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)

**Deterministic trust scoring for MCP servers.**

`MCP Trust Kit` scans a local MCP server over `stdio`, checks protocol and tool hygiene, flags
risky tool surface, calculates a trust score, and writes terminal, JSON, and SARIF output.

## Why

MCP servers expose tools to agents. Basic hygiene and risky capability review should be easy to
run in CI.

`MCP Trust Kit` gives you a fast, explainable signal before you wire a server into automation.

## Quickstart Local

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e .[dev]
.\.venv\Scripts\mcp-trust scan --cmd .\.venv\Scripts\python examples\insecure-server\server.py
```

Write JSON and SARIF and fail below a threshold:

```powershell
.\.venv\Scripts\mcp-trust scan `
  --min-score 80 `
  --json-out mcp-trust-report.json `
  --sarif mcp-trust-report.sarif `
  --cmd .\.venv\Scripts\python examples\insecure-server\server.py
```

## GitHub Actions Quickstart

```yaml
name: MCP Trust Scan

on:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read
  security-events: write

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run MCP Trust Kit
        uses: <owner>/mcp-trust-kit@v0.3.0
        with:
          cmd: python path/to/your/server.py
          min-score: "80"
          json-out: mcp-trust-report.json
          sarif-out: mcp-trust-report.sarif

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: mcp-trust-report.sarif
```

Replace `<owner>/mcp-trust-kit@v0.3.0` with the real published action reference.

## Example Output

```text
Server: Insecure Demo Server
Version: 0.1.0
Protocol: 2025-11-25
Target: stdio:[".\\.venv\\Scripts\\python","examples\\insecure-server\\server.py"]
Tools: 4
Findings: 4
Severity: error=2, warning=2, info=0
Total Score: 40/100
Category Scores:
- spec: 100/100 (penalties: 0)
- auth: 100/100 (penalties: 0)
- secrets: 100/100 (penalties: 0)
- tool_surface: 40/100 (penalties: 60)
Top Findings:
- WARNING vague_tool_description [do_it]: Tool 'do_it' uses a vague description that does not explain its behavior clearly.
- WARNING weak_input_schema [debug_payload]: Tool 'debug_payload' exposes a weak input schema that accepts poorly constrained input.
- ERROR dangerous_exec_tool [exec_command]: Tool 'exec_command' appears to expose host command execution.
- ERROR dangerous_fs_write_tool [write_file]: Tool 'write_file' appears to provide filesystem write access.
```

## Rule Categories

- Protocol and tool hygiene:
  duplicate names, missing descriptions, vague descriptions, weak input schemas
- Risky tool surface:
  exec-like tools and filesystem write tools
- Score buckets:
  `spec`, `auth`, `secrets`, `tool_surface`

## Examples And Sample Reports

- [examples/insecure-server/README.md](examples/insecure-server/README.md)
- [examples/fake_stdio_server.py](examples/fake_stdio_server.py)
- [sample-reports/insecure-server.report.json](sample-reports/insecure-server.report.json)
- [sample-reports/insecure-server.report.sarif](sample-reports/insecure-server.report.sarif)
- [sample-reports/insecure-server.terminal.md](sample-reports/insecure-server.terminal.md)
- [docs/architecture.md](docs/architecture.md)
- [.github/workflows/example.yml](.github/workflows/example.yml)

## Roadmap

- expand deterministic rules for `spec`, `auth`, and `secrets`
- improve SARIF location mapping where source context is available
- add more sample reports and demo fixtures
- keep the GitHub Action path simple and reliable

## Contributing

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e .[dev]
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\python -m ruff check .
.\.venv\Scripts\python -m mypy
```

Focused contributions are best: new deterministic rules, better `stdio` transport hardening,
reporter improvements, docs, and examples.

## License

Apache-2.0. See [LICENSE](LICENSE).
