from fastapi import FastAPI
from fastapi.responses import JSONResponse
from init.load_data import get_po_tracking_data, load_po_tracking_data
import os
import numpy as np
import pandas as pd

print("[DEBUG] Initializing FastAPI app...")
app = FastAPI()
print("[DEBUG] FastAPI app initialized. Ready to start server.")

@app.get("/summary")
def get_summary():
    # Load PO tracking data
    csv_path = os.path.join("dataset", "po_data_summary.csv")
    print(f"[DEBUG] Loading PO tracking data from: {csv_path}")
    response = get_po_tracking_data(csv_path)

    if response is None:
        print("[DEBUG] PO tracking data not found.")
        return JSONResponse(content={"error": "PO tracking data not found."}, status_code=404)

    return JSONResponse(response)

@app.get("/po/{po_id}")
def get_po(po_id: str):
    # Load PO tracking data
    csv_path = os.path.join("dataset", "po_data_summary.csv")
    print(f"[DEBUG] Loading PO tracking data from: {csv_path}")
    df = load_po_tracking_data(csv_path)
    if df is None:
        print("[DEBUG] PO tracking data not found.")
        return JSONResponse(content={"error": "PO tracking data not found."}, status_code=404)
    # Filter for the specific PO ID
    po_row = df[df['po_id'] == po_id]
    if po_row.empty:
        print(f"[DEBUG] PO ID {po_id} not found.")
        return JSONResponse(content={"error": f"PO ID {po_id} not found."}, status_code=404)
    # Replace non-JSON-compliant values
    po_row = po_row.replace([np.inf, -np.inf], np.nan).where(pd.notnull(po_row), None)
    print(f"[DEBUG] Returning data for PO ID: {po_id}")
    return JSONResponse(content=po_row.to_dict(orient="records")[0]) 


print(get_summary())