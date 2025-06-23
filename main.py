from fastapi import FastAPI
from fastapi.responses import JSONResponse
from init.load_data import load_po_tracking_data, dataframe_to_json
import os

app = FastAPI()

@app.get("/summary")
def get_summary():
    # Load PO tracking data
    csv_path = os.path.join("sample_data", "po_tracking_data.csv")
    df = load_po_tracking_data(csv_path)
    if df is None:
        return JSONResponse(content={"error": "PO tracking data not found."}, status_code=404)
    # Return the summary (all data as JSON for now)
    return JSONResponse(content={"summary": df.to_dict(orient="records")})

@app.get("/po/{po_id}")
def get_po(po_id: str):
    # Load PO tracking data
    csv_path = os.path.join("sample_data", "po_tracking_data.csv")
    df = load_po_tracking_data(csv_path)
    if df is None:
        return JSONResponse(content={"error": "PO tracking data not found."}, status_code=404)
    # Filter for the specific PO ID
    po_row = df[df['po_id'] == po_id]
    if po_row.empty:
        return JSONResponse(content={"error": f"PO ID {po_id} not found."}, status_code=404)
    return JSONResponse(content=po_row.to_dict(orient="records")[0]) 