# Validated On Real MCP Servers

This note records a few reproducible validation runs on public MCP servers.

It is not a leaderboard and it is not a claim that a low score means a server is "bad".
The point is narrower: show that `MCP Trust Kit` works on real servers outside the demo fixture.

Validation date: `2026-03-29`

Reference sources for the public packages used here:

- official servers repo: https://github.com/modelcontextprotocol/servers
- official project site: https://modelcontextprotocol.io

## Environment Note

These validation runs were executed on Windows.

- `mcp-trust` launches subprocesses without a shell
- on this machine `npx` resolves through `npx.cmd`
- on macOS or Linux, the equivalent command is usually just `npx`

## 1. Deterministic Demo Fixture

Server:

- [`examples/insecure-server`](../examples/insecure-server/README.md)

Command:

```powershell
.\.venv\Scripts\mcp-trust scan --cmd .\.venv\Scripts\python examples\insecure-server\server.py
```

Observed result:

- score: `40/100`
- findings:
  - `vague_tool_description`
  - `weak_input_schema`
  - `dangerous_exec_tool`
  - `dangerous_fs_write_tool`

Caveat:

- this server is intentionally insecure and exists as a stable demo/test asset

## 2. Official Memory Server

Package:

- `@modelcontextprotocol/server-memory@2026.1.26`

Command used on Windows:

```powershell
.\.venv\Scripts\mcp-trust scan --cmd C:\nvm4w\nodejs\npx.cmd -y @modelcontextprotocol/server-memory@2026.1.26
```

Observed result:

- server name: `memory-server`
- score: `90/100`
- finding count: `1`
- rule hit:
  - `weak_input_schema` on `read_graph`

Why this is still a "good" case:

- no dangerous exec-like tools were flagged
- no filesystem write tools were flagged
- descriptions and most schemas were clear

Caveat:

- the current `weak_input_schema` rule treats an empty object schema as a warning
- that is a deliberate v0.3.0 heuristic, not a claim that the server is unsafe

## 3. Official Filesystem Server

Package:

- `@modelcontextprotocol/server-filesystem@2026.1.14`

Command used on Windows:

```powershell
$tmp = Join-Path $PWD ".tmp-mcp-fs"
New-Item -ItemType Directory -Force $tmp | Out-Null
.\.venv\Scripts\mcp-trust scan --cmd C:\nvm4w\nodejs\npx.cmd -y @modelcontextprotocol/server-filesystem@2026.1.14 $tmp
```

Observed result:

- server name: `secure-filesystem-server`
- score: `30/100`
- finding count: `4`
- rule hits:
  - `weak_input_schema` on `list_allowed_directories`
  - `dangerous_fs_write_tool` on `write_file`
  - `dangerous_fs_write_tool` on `edit_file`
  - `dangerous_fs_write_tool` on `create_directory`

Why this is a useful "risky" case:

- the server legitimately exposes filesystem mutation tools
- the low score reflects risky tool surface, not exploitability
- this is exactly the kind of capability that many teams want surfaced in CI

Caveat:

- this server can still be entirely appropriate in a constrained environment
- `MCP Trust Kit` scores surface risk, not business intent

## How To Read These Results

- a high score is not a guarantee of safety
- a low score is not a public accusation
- the findings are best used as a review signal before adoption
