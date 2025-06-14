"""Agent SDK for common helper functions (stub)."""

from typing import Any


def publish_event(topic: str, event: dict) -> None:
    """Publish an event to message bus (stub)."""
    import logging
    logging.getLogger(__name__).info("Publish to %s: %s", topic, event)
