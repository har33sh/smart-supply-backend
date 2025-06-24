# # watch.py  – run locally once
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery   import build

# SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# flow   = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
# creds  = flow.run_local_server(port=0)

# gmail  = build("gmail", "v1", credentials=creds)
# gmail.users().watch(
#     userId="me",
#     body={
#         "topicName": "projects/mail-mvp-123/topics/new-mail",
#         "labelIds": ["INBOX"]          # limit to inbox only
#     }).execute()                       # returns startHistoryId


# watch.py  – run once from the SAME folder where inbound.py lives
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery   import build
import json, pathlib

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
flow   = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
creds  = flow.run_local_server(port=0)

# ▼▼  save the credential blob so FastAPI can read it later  ▼▼
path = pathlib.Path(__file__).with_name("token.json")
path.write_text(creds.to_json())
print(f"✅  token.json written to {path.resolve()}")

gmail = build("gmail", "v1", credentials=creds)
resp  = gmail.users().watch(
    userId="me",
    body={
        "topicName": "projects/mail-mvp-123/topics/new-mail",
        "labelIds": ["INBOX"]
    }).execute()

print("📡  Watch registered → startHistoryId:", resp["historyId"])
