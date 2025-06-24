# Smart Supply Backend

A simple FastAPI backend with two endpoints:

- `/summary` — Returns a JSON summary.
- `/po/{po_id}` — Returns JSON with the provided PO ID and example details.

## Setup

1. **Clone the repository**
2. **(Optional) Set up Google Authentication**
   - Place your `client_secret.json` and `token.json` files in the root of the project directory. These are required for Google API access.
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **(Optional) Set up environment variables**
   - Copy `.env.example` to `.env` and edit as needed.
5. **Place your PO tracking data CSV**
   - The file should be located at `dataset/po_data_summary/po_tracking_data.csv`.

## Running the Server

```bash
uvicorn main:app --reload
```

## Endpoints

- `GET /summary`
  - Returns: All PO summary data as JSON from the CSV.
- `GET /po/{po_id}`
  - Returns: Details for the specified PO ID from the CSV.

---

- Python `.venv` and other common files are ignored via `.gitignore`. 