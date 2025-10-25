# backend/api/routes/ingestion.py
import uuid
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from api.services.document_processor import DocumentProcessor
from api.services.schema_discovery import SchemaDiscovery

router = APIRouter()

# in-memory tracker for uploads
INGESTION_JOBS = {}
UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ingest/documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload multiple documents and process them sequentially."""
    job_id = str(uuid.uuid4())
    INGESTION_JOBS[job_id] = {"status": "processing", "processed": 0, "total": len(files), "errors": []}
    processor = DocumentProcessor(upload_dir=UPLOAD_DIR)

    for idx, up in enumerate(files):
        try:
            dest_path = os.path.join(UPLOAD_DIR, f"{job_id}_{idx}_{up.filename}")
            with open(dest_path, "wb") as f:
                content = await up.read()
                f.write(content)
            processor.process_document(dest_path)
            INGESTION_JOBS[job_id]["processed"] += 1
        except Exception as e:
            INGESTION_JOBS[job_id]["errors"].append({"file": up.filename, "error": str(e)})

    INGESTION_JOBS[job_id]["status"] = (
        "completed" if not INGESTION_JOBS[job_id]["errors"] else "completed_with_errors"
    )
    return {"job_id": job_id, "status": INGESTION_JOBS[job_id]["status"]}

@router.get("/ingest/status/{job_id}")
def ingestion_status(job_id: str):
    job = INGESTION_JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found")
    return job

@router.post("/ingest/database")
def ingest_database(connection_string: str = Form(...)):
    """Test DB connection and discover schema dynamically."""
    try:
        schema = SchemaDiscovery(connection_string=connection_string).analyze_database()
        return {"ok": True, "schema": schema}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to connect: {e}")
