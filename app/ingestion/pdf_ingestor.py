# Placeholder for PDF ingestion logicimport fitz
from app.db.supabase import supabase


def chunk_text(text, size=1000):
    return [
        text[i:i+size]
        for i in range(0, len(text), size)
    ]


def ingest_pdf(file_path, file_name):
    doc = fitz.open(file_path)

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()

        chunks = chunk_text(text)

        for chunk in chunks:
            if chunk.strip():
                supabase.table("documents").insert({
                    "file_name": file_name,
                    "page_number": page_num,
                    "chunk_text": chunk
                }).execute()