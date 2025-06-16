"""Agent SDK for common helper functions."""

from __future__ import annotations

import json
import logging
import os
from typing import Generator

from kafka import KafkaConsumer, KafkaProducer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_producer: KafkaProducer | None = None


def get_producer() -> KafkaProducer:
    """Return a cached Kafka producer using ``KAFKA_BOOTSTRAP`` env var."""

    global _producer
    if _producer is None:
        if os.getenv("NO_KAFKA") == "1":
            class DummyProducer:
                def send(self, *_, **__):
                    return None

                def flush(self):
                    return None

            _producer = DummyProducer()  # type: ignore[assignment]
        else:
            bootstrap = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
            _producer = KafkaProducer(
                bootstrap_servers=bootstrap,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
    return _producer


def publish_event(topic: str, event: dict) -> None:
    """Publish an event to the Kafka bus."""

    producer = get_producer()
    try:
        producer.send(topic, event)
        producer.flush()
        logger.info("Publish to %s: %s", topic, event)
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("Kafka publish failed: %s", exc)


def subscribe(topic: str) -> Generator[dict, None, None]:
    """Subscribe to events on the given topic and yield them as dicts."""

    if os.getenv("NO_KAFKA") == "1":
        return

    bootstrap = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=os.getenv("KAFKA_GROUP", "agentsdk"),
    )
    for msg in consumer:
        yield msg.value
