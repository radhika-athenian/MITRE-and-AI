from fastapi import FastAPI
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()



class Alert(BaseModel):
    id: str
    description: str
    severity: int


def publish_alert(alert: Alert):
    """Stub for publishing alerts to a message bus."""
    try:
        # Here you would publish to Kafka or another message bus
        logger.info("Publishing alert: %s", alert.json())
    except Exception as exc:
        logger.error("Failed to publish alert: %s", exc)


@app.post("/alerts")
async def receive_alert(alert: Alert):
    publish_alert(alert)
    return {"status": "received"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
