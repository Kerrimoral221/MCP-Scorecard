# Insecure Server Terminal Output

Generated with:

```powershell
.\.venv\Scripts\mcp-trust scan --cmd .\.venv\Scripts\python examples\insecure-server\server.py
```

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
