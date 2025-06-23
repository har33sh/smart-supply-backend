from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/summary")
def get_summary():
    # Example summary data
    return JSONResponse(content={"summary": "This is a summary."})

@app.get("/po/{po_id}")
def get_po(po_id: str):
    # Example PO data
    return JSONResponse(content={"po_id": po_id, "details": "Details for PO."}) 