import logging
from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.data_store import InMemoryDB
from info_extractor.email import analyze_email_with_openrouter
from info_extractor.document import analyze_document
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Initializing FastAPI app...")
app = FastAPI()
logger.debug("FastAPI app initialized. Ready to start server.")

@app.on_event("startup")
def load_po_data():
    json_path = os.path.join("dataset", "po_data.json")
    InMemoryDB.load_data(json_path)
    logger.debug("PO data loaded into in-memory database.")

class EmailExtractionRequest(BaseModel):
    email_text: str

class DocumentExtractionRequest(BaseModel):
    document_text: str

@app.get("/summary")
def get_summary():
    records = InMemoryDB.get_all()
    if not records:
        logger.debug("PO tracking data not found.")
        return JSONResponse(content={"error": "PO tracking data not found."}, status_code=404)
    return JSONResponse(content=records)

@app.get("/po/{po_id}")
def get_po(po_id: str):
    record = InMemoryDB.get_by_po_number(po_id)
    if not record:
        logger.debug(f"PO ID {po_id} not found.")
        return JSONResponse(content={"error": f"PO ID {po_id} not found."}, status_code=404)
    logger.debug(f"Returning data for PO ID: {po_id}")
    return JSONResponse(content=record)

@app.post("/extract-email-info", summary="Extract info from email text", response_description="Extracted info as JSON")
async def extract_email_info(payload: EmailExtractionRequest = Body(...)):
    if not payload.email_text:
        return JSONResponse(content={"error": "email_text is required"}, status_code=400)
    try:
        result = analyze_email_with_openrouter(payload.email_text)
        return JSONResponse(content={"result": result})
    except Exception as e:
        logger.error(f"Error extracting email info: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/extract-document-info", summary="Extract info from a document")
def extract_document_info(payload: DocumentExtractionRequest):
    logger.info("Received request to analyze document.")
    result = analyze_document(payload.document_text)
    return JSONResponse(content={"result": result}) 
