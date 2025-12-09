import logging
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from src.webhooks.verify import verify_signature
from src.utils.storage import save_webhook_event

logger = logging.getLogger(__name__)
router = APIRouter()

class WebhookPayload(BaseModel):
    event_type: str
    delivery_id: str
    data: dict

@router.post("/test")
async def webhook_test(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None),
    x_github_delivery: Optional[str] = Header(None),
):
    """
    Minimal webhook endpoint with signature verification and persistence
    """
    body = await request.body()
    
    # Verify signature if present
    if x_hub_signature_256:
        if not verify_signature(body, x_hub_signature_256):
            logger.warning(f"Invalid signature for delivery {x_github_delivery}")
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse payload
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Log structured event
    event_data = {
        "delivery_id": x_github_delivery or "unknown",
        "event_type": payload.get("action", "test"),
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload,
    }
    
    logger.info(
        "Webhook received",
        extra={
            "delivery_id": event_data["delivery_id"],
            "event_type": event_data["event_type"],
        }
    )
    
    # Persist event
    event_id = save_webhook_event(event_data)
    
    return {
        "status": "received",
        "event_id": event_id,
        "delivery_id": event_data["delivery_id"],
        "message": "Webhook processed successfully"
    }
