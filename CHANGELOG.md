# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project uses Semantic Versioning.

## [0.3.0] - 2026-03-29

Initial public release.

### Added

- local `stdio` MCP discovery transport with deterministic handshake and tool listing
- normalized data models for servers, tools, findings, reports, and score breakdowns
- deterministic v0 ruleset for tool hygiene and risky tool surface
- stable penalty-based scoring engine with category breakdowns
- terminal summary, JSON report, and SARIF export
- `mcp-trust scan` CLI with score gating and release-friendly exit codes
- composite GitHub Action for CI usage
- demo MCP servers, sample reports, and release docs

### Changed

- release surface hardened for public GitHub usage
- README rewritten for quickstart, GitHub Actions, scoring, and sample artifacts

### Fixed

- CLI examples aligned on `--cmd`
- sample artifacts regenerated from current real scanner behavior
- package license metadata normalized to SPDX form for distribution metadata
