# PDF Upload API Endpoint
# Handles PDF file uploads and document ingestion

import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.ingestion.pdf_ingestor import ingest_pdf

router = APIRouter(tags=["Document Management"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and ingest a PDF document.
    
    This endpoint accepts PDF files, saves them, extracts text, chunks it,
    and stores it in Supabase for later retrieval.
    
    Args:
        file (UploadFile): PDF file to upload
    
    Returns:
        dict: Upload confirmation with file name
    
    Raises:
        HTTPException: If file is not a PDF
    
    Example:
        ```bash
        curl -X POST "http://localhost:8001/upload" \
          -F "file=@document.pdf"
        ```
    
    Response:
        ```json
        {
          "message": "Uploaded and indexed",
          "file": "document.pdf"
        }
        ```
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Save file to uploads directory
    path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(path, "wb") as f:
        f.write(await file.read())

    # Process and index the PDF
    ingest_pdf(path, file.filename)

    return {
        "message": "Uploaded and indexed successfully",
        "file": file.filename
    }
