"""Transport interfaces and transport-specific error types."""

from __future__ import annotations

from typing import Protocol, TypeVar

from mcp_trust.models import NormalizedServer

TransportTargetT = TypeVar("TransportTargetT", contravariant=True)


class TransportError(RuntimeError):
    """Base error raised by transport implementations."""


class ServerStartupError(TransportError):
    """Raised when a server process cannot be started or exits too early."""


class ProtocolError(TransportError):
    """Raised when a server speaks invalid or unsupported MCP JSON-RPC."""


class TransportTimeoutError(TransportError):
    """Raised when a transport operation does not complete within the timeout."""


class Transport(Protocol[TransportTargetT]):
    """Load a transport-specific target and return normalized server data."""

    transport_name: str

    def scan(self, target: TransportTargetT) -> NormalizedServer:
        """Scan the given target and return normalized data for scoring."""
