# Smart Supply Backend

A simple FastAPI backend with two endpoints:

- `/summary` — Returns a JSON summary.
- `/po/{po_id}` — Returns JSON with the provided PO ID and example details.

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **(Optional) Set up environment variables**
   - Copy `.env.example` to `.env` and edit as needed.

## Running the Server

```bash
uvicorn main:app --reload
```

## Endpoints

- `GET /summary`
  - Returns: `{ "summary": "This is a summary." }`
- `GET /po/{po_id}`
  - Returns: `{ "po_id": "<po_id>", "details": "Details for PO." }`

---

- Python `.venv` and other common files are ignored via `.gitignore`. 