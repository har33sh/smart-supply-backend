# rewatch.py  – one-time helper for the demo
from google.oauth2.credentials import Credentials
from googleapiclient.discovery  import build
import google.auth.transport.requests as tr

PROJECT = "mail-mvp-123"                       # ← your Cloud project ID
TOPIC   = f"projects/{PROJECT}/topics/new-mail"
TOKEN   = "token.json"
SCOPES  = ["https://www.googleapis.com/auth/gmail.readonly"]

creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
creds.refresh(tr.Request())
gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)

# stop old watch (ignore error if none)
try:
    gmail.users().stop(userId="me").execute()
except Exception:
    pass

resp = gmail.users().watch(
    userId="me",
    body={"topicName": TOPIC, "labelIds": ["INBOX"]}
).execute()

print("✅ watch registered — expires:", resp['expiration'])
