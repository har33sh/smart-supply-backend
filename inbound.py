# inbound.py  – verbose debug edition
import os, json, base64, re, html, logging, textwrap
from fastapi import FastAPI, Request, HTTPException
import google.auth.transport.requests
import google.oauth2.id_token
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

###############################################################################
# CONFIG
###############################################################################
AUDIENCE   = os.getenv("PUSH_AUDIENCE")           # must match pushEndpoint
TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "token.json")
SCOPES     = ["https://www.googleapis.com/auth/gmail.readonly"]

if not AUDIENCE:
    raise RuntimeError("Set PUSH_AUDIENCE env var (your ngrok URL + /inbound)")

###############################################################################
# LOGGING
###############################################################################
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("inbound")

###############################################################################
# APP + HELPERS
###############################################################################
app = FastAPI()

def verify_jwt(bearer_header: str) -> None:
    token = bearer_header.split()[1]  # strip "Bearer "
    req   = google.auth.transport.requests.Request()
    info  = google.oauth2.id_token.verify_oauth2_token(token, req, AUDIENCE)
    log.debug("JWT verified. aud=%s, sub=%s, exp=%s", info["aud"], info["sub"], info["exp"])

def gmail_service() -> "googleapiclient.discovery.Resource":
    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    except FileNotFoundError:
        log.error("token.json missing – run watch.py again")
        raise HTTPException(500, "Server not initialised")
    try:
        creds.refresh(google.auth.transport.requests.Request())
    except RefreshError as e:
        log.error("OAuth refresh failed: %s – run watch.py again", e)
        raise HTTPException(500, "Token expired")
    return build("gmail", "v1", credentials=creds, cache_discovery=False)

def extract_body(payload: dict) -> str:
    """Return plaintext body, or HTML stripped to text."""
    if payload.get("mimeType") == "text/plain":
        return payload.get("body", {}).get("data", "")
    if "parts" in payload:
        for p in payload["parts"]:
            data = extract_body(p)
            if data:
                return data
    return ""

def decode_b64(data: str) -> str:
    try:
        return base64.urlsafe_b64decode(data).decode(errors="ignore")
    except Exception:
        return "(decode error)"

###############################################################################
# ROUTE
###############################################################################
@app.post("/inbound")
async def inbound(request: Request):
    # ─── 1. verify JWT ───────────────────────────────────────────────────────
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(401, "No auth header")
    verify_jwt(auth)
    log.info("✅ JWT verified")

    # ─── 2. decode envelope ─────────────────────────────────────────────────
    body_json = await request.json()
    envelope_raw = base64.b64decode(body_json["message"]["data"]).decode()
    envelope    = json.loads(envelope_raw)
    log.info("📦 Envelope: %s", envelope)

    history_id = envelope.get("historyId")
    if not history_id:
        log.info("ℹ️  No historyId (sync/test message) – ignoring")
        return {"status": "ignored"}

    # ─── 3. call Gmail API for deltas ───────────────────────────────────────
    gmail = gmail_service()
    log.info("🔍 history.list startHistoryId=%s", history_id)
    hist = gmail.users().history().list(
        userId="me",
        startHistoryId=history_id,
        historyTypes=["messageAdded"],
        maxResults=100,
    ).execute()

    changes = hist.get("history", [])
    log.info("🔍 history.list returned %d change(s)", len(changes))

    # fallback: if no changes, fetch the single latest message (never silent)
    if not changes:
        latest_id = gmail.users().messages().list(
            userId="me", maxResults=1).execute()["messages"][0]["id"]
        changes = [{"messages": [{"id": latest_id}]}]
        log.info("⚠️  Using fallback latest message id=%s", latest_id)

    # ─── 4. print every message in full detail ──────────────────────────────
    for change in changes:
        msg_id = change["messages"][0]["id"]
        msg    = gmail.users().messages().get(
                    userId="me", id=msg_id, format="full").execute()

        hdrs = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        sender   = hdrs.get("From", "(unknown)")
        subject  = hdrs.get("Subject", "(no subject)")

        raw_body = extract_body(msg["payload"]) or msg.get("snippet", "")
        decoded  = decode_b64(raw_body)
        text     = html.unescape(re.sub(r"<[^>]+>", "", decoded)).strip()

        log.info("=" * 72)
        log.info("\n%s\n%s",
                 textwrap.dedent(f"""
                 Gmail-ID : {msg_id}
                 From     : {sender}
                 Subject  : {subject}
                 Body     : {text[:500].replace(chr(10), ' ')}{' …' if len(text)>500 else ''}
                 """).rstrip())
        
        log.info("=" * 72)

    return {"status": "ok"}          # 200 tells Pub/Sub to ack
