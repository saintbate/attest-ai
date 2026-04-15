"""Attest — EU AI Act compliance SDK for AI systems."""

__version__ = "0.1.0"

from attest.sdk.wrapper import wrap, track, monitor
from attest.sdk.registry import get_registry

__all__ = ["wrap", "track", "monitor", "get_registry"]
