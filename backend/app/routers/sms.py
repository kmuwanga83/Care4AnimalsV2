from fastapi import APIRouter
from ..schemas import SmsWebhookIn
from ..services.sms_engine import build_sms_response

router = APIRouter(prefix="/api/v1/sms", tags=["sms"])

@router.post("/webhook")
def sms_webhook(payload: SmsWebhookIn):
    reply = build_sms_response(payload.text)
    return {"to": payload.from_number, "reply": reply}
