"""FastAPI backend."""
import logging
import os
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from app.models import ResumeData, UploadResponse
from app.services.parser import extract_resume_text
from app.services.llm_service import extract_resume_with_llm
from app.utils.logger import configure_logging

load_dotenv()
configure_logging()
logger = logging.getLogger(__name__)
app = FastAPI(title="AI Resume Parser API", version="1.0.0")
# Demo storage: data is lost when the backend restarts.
RESUME_STORE: dict[str, ResumeData] = {}
MAX_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))

@app.get("/health")
def health() -> dict[str, str]:
    """Check that the API is running."""
    return {"status": "ok"}

@app.post("/api/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)) -> UploadResponse:
    """Upload a PDF/DOCX, extract information, and return a unique ID."""
    filename = file.filename or ""
    if not filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(400, "Upload a PDF or DOCX file.")
    content = await file.read()
    if not content:
        raise HTTPException(400, "Uploaded file is empty.")
    if len(content) > MAX_MB * 1024 * 1024:
        raise HTTPException(413, f"File exceeds the {MAX_MB} MB limit.")
    try:
        text = extract_resume_text(filename, content)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    try:
        resume = extract_resume_with_llm(text)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc
    except Exception as exc:
        logger.exception("LLM extraction failed")
        raise HTTPException(502, "LLM extraction failed. Check API configuration and retry.") from exc
    document_id = str(uuid4())
    RESUME_STORE[document_id] = resume
    logger.info("Resume parsed successfully document_id=%s", document_id)
    return UploadResponse(document_id=document_id, resume=resume)

@app.get("/api/resume/{document_id}", response_model=UploadResponse)
def get_resume(document_id: str) -> UploadResponse:
    """Retrieve a parsed resume by document ID."""
    if document_id not in RESUME_STORE:
        raise HTTPException(404, "Resume not found for this document ID.")
    return UploadResponse(document_id=document_id, resume=RESUME_STORE[document_id])
