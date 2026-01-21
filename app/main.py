import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from app.core.config import settings
from app.db.models import init_db
from app.db.storage import insert_message, fetch_messages, fetch_stats
from app.core.logging import log_request
from app.core.metrics import webhook_requests_total

app = FastAPI()
app.middleware("http")(log_request)

init_db()


class WebhookPayload(BaseModel):
    message_id: str
    from_: str = Field(alias="from")
    to: str
    ts: str
    text: str | None = None


@app.get("/health/live")
def live():
    return {"status": "live"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/webhook")
async def webhook(request: Request):
    raw = await request.body()
    signature = request.headers.get("X-Signature")

    expected = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        raw,
        hashlib.sha256,
    ).hexdigest()

    if not signature or not hmac.compare_digest(signature, expected):
        webhook_requests_total.labels("invalid_signature").inc()
        raise HTTPException(status_code=401, detail="invalid signature")

    payload = await request.json()
    created = insert_message(payload)

    webhook_requests_total.labels(
        "created" if created else "duplicate"
    ).inc()

    return {"status": "ok"}


@app.get("/messages")
def messages(limit: int = 50, offset: int = 0, from_: str | None = None, since: str | None = None, q: str | None = None):
    return fetch_messages(limit, offset, from_, since, q)


@app.get("/stats")
def stats():
    return fetch_stats()


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    from prometheus_client import generate_latest
    return generate_latest()

