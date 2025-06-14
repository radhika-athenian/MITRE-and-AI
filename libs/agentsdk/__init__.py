"""Agent SDK for common helper functions."""

from __future__ import annotations

import json
import logging
import os
from typing import Generator

import redis

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_redis_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    """Return a cached Redis client using ``REDIS_URL`` env var."""

    global _redis_client
    if _redis_client is None:
        url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        _redis_client = redis.Redis.from_url(url)
    return _redis_client


def publish_event(topic: str, event: dict) -> None:
    """Publish an event to the Redis pub/sub bus."""

    client = get_redis()
    client.publish(topic, json.dumps(event))
    logger.info("Publish to %s: %s", topic, event)


def subscribe(topic: str) -> Generator[dict, None, None]:
    """Subscribe to events on the given topic and yield them as dicts."""

    client = get_redis()
    pubsub = client.pubsub()
    pubsub.subscribe(topic)
    for message in pubsub.listen():
        if message.get("type") == "message":
            data = json.loads(message["data"])
            yield data
