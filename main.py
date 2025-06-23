import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils.load_data import get_all_po_records, get_po_record_by_number
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Initializing FastAPI app...")
app = FastAPI()
logger.debug("FastAPI app initialized. Ready to start server.")

@app.get("/summary")
def get_summary():
    csv_path = os.path.join("dataset", "po_data_summary.csv")
    logger.debug(f"Loading PO tracking data from: {csv_path}")
    records = get_all_po_records(csv_path)
    if records is None:
        logger.debug("PO tracking data not found.")
        return JSONResponse(content={"error": "PO tracking data not found."}, status_code=404)
    return JSONResponse(content=records)

@app.get("/po/{po_id}")
def get_po(po_id: str):
    csv_path = os.path.join("dataset", "po_data_summary.csv")
    logger.debug(f"Loading PO tracking data from: {csv_path}")
    record = get_po_record_by_number(po_id, csv_path)
    if record is None:
        logger.debug(f"PO ID {po_id} not found.")
        return JSONResponse(content={"error": f"PO ID {po_id} not found."}, status_code=404)
    logger.debug(f"Returning data for PO ID: {po_id}")
    return JSONResponse(content=record) 
