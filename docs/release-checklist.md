# Release Checklist

Use this list before publishing `v0.3.0`.

## Repository

- confirm the default branch is green
- replace README badge placeholders with the real GitHub owner and repository
- replace the README action reference placeholder with the real published tag
- verify `LICENSE`, `CHANGELOG.md`, and release docs are present

## Validation

- run `python -m venv .venv`
- run `.\.venv\Scripts\activate`
- run `pip install -e .[dev]`
- run `.\.venv\Scripts\python -m pytest`
- run `.\.venv\Scripts\python -m ruff check .`
- run `.\.venv\Scripts\python -m mypy`
- run `.\.venv\Scripts\mcp-trust --help`
- run `.\.venv\Scripts\mcp-trust scan --help`

## Install Surface

- create a clean virtual environment
- run `pip install .`
- run `mcp-trust --help`
- verify `import mcp_trust; print(mcp_trust.__version__)`
- verify package metadata shows version `0.3.0`

## Examples And Reports

- run `.\.venv\Scripts\mcp-trust scan --cmd .\.venv\Scripts\python examples\insecure-server\server.py`
- run `.\.venv\Scripts\mcp-trust scan --json-out sample-reports\insecure-server.report.json --sarif sample-reports\insecure-server.report.sarif --cmd .\.venv\Scripts\python examples\insecure-server\server.py`
- confirm JSON, SARIF, and terminal sample artifacts match current output
- confirm `examples/insecure-server/README.md` matches the current CLI syntax

## GitHub Action

- verify `action.yml` inputs are `cmd`, `min-score`, `json-out`, `sarif-out`
- verify `.github/workflows/example.yml` is copy-pasteable
- verify SARIF upload example still points to `github/codeql-action/upload-sarif@v3`

## Release

- create tag `v0.3.0`
- publish GitHub Release notes from `CHANGELOG.md`
- attach or link sample artifacts if desired
- smoke-test the published action from a separate repository
