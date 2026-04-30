import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.ingestion.pdf_ingestor import ingest_pdf

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF allowed"
        )

    path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(path, "wb") as f:
        f.write(await file.read())

    ingest_pdf(path, file.filename)

    return {
        "message": "Uploaded and indexed",
        "file": file.filename
    }