"""Ingest service for receiving alerts and classifying them."""

from __future__ import annotations

import logging
import os
import time
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from agentsdk import publish_event

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


app = FastAPI()


class Alert(BaseModel):
    id: str
    description: str
    severity: int


class ClassifiedAlert(Alert):
    """Alert enriched with ATT&CK technique and asset information."""

    technique_id: str
    asset_id: str
    timestamp: float


def classify_alert(alert: Alert) -> ClassifiedAlert:
    """Classify the alert using an LLM (stub).

    The real implementation would call the OpenAI API. For now this returns
    static values so unit tests can run without network access or credentials.
    """

    _ = os.getenv("OPENAI_API_KEY")
    technique_id = "T0001"
    asset_id = "asset-123"
    return ClassifiedAlert(
        id=alert.id,
        description=alert.description,
        severity=alert.severity,
        technique_id=technique_id,
        asset_id=asset_id,
        timestamp=time.time(),
    )


def publish_alert(alert: ClassifiedAlert) -> None:
    """Publish the classified alert to a message bus (stub)."""
    try:
        publish_event("alerts", alert.dict())
    except Exception as exc:  # pragma: no cover - logging only
        logger.error("Failed to publish alert: %s", exc)


@app.post("/alerts")
async def receive_alert(alert: Alert):
    classified = classify_alert(alert)
    publish_alert(classified)
    return {"status": "received", "technique_id": classified.technique_id,
            "asset_id": classified.asset_id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("INGEST_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
