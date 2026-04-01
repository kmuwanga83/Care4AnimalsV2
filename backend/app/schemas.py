from pydantic import BaseModel

class SmsWebhookIn(BaseModel):
    from_number: str
    text: str
