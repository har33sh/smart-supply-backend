import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from init.load_data import get_po_tracking_data, load_po_tracking_data
import os
import numpy as np
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Initializing FastAPI app...")
app = FastAPI()
logger.debug("FastAPI app initialized. Ready to start server.")

def clean_nans(obj):
    if isinstance(obj, dict):
        return {k: clean_nans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nans(v) for v in obj]
    elif isinstance(obj, float):
        if np.isnan(obj) or obj in [np.inf, -np.inf]:
            return None
        return obj
    else:
        return obj

@app.get("/summary")
def get_summary():
    # Load PO tracking data
    csv_path = os.path.join("dataset", "po_data_summary.csv")
    logger.debug(f"Loading PO tracking data from: {csv_path}")
    response = get_po_tracking_data(csv_path)

    if response is None:
        logger.debug("PO tracking data not found.")
        return JSONResponse(content={"error": "PO tracking data not found."}, status_code=404)

    return JSONResponse(content=response)

@app.get("/po/{po_id}")
def get_po(po_id: str):
    csv_path = os.path.join("dataset", "po_data_summary.csv")
    logger.debug(f"Loading PO tracking data from: {csv_path}")
    df = load_po_tracking_data(csv_path)
    if df is None:
        logger.debug("PO tracking data not found.")
        return JSONResponse(content={"error": "PO tracking data not found."}, status_code=404)
    # Filter for the specific PO ID
    po_row = df[df['po_number'] == po_id]
    logger.debug(f"Filtered PO row: {po_row}")
    if po_row.empty:
        logger.debug(f"PO ID {po_id} not found.")
        return JSONResponse(content={"error": f"PO ID {po_id} not found."}, status_code=404)
    # Convert to dict and clean NaNs/Infs
    record = po_row.to_dict(orient="records")[0]
    record = clean_nans(record)
    logger.debug(f"Returning data for PO ID: {po_id}")
    return JSONResponse(content=record) 
