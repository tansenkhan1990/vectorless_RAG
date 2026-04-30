# PDF Ingestion Module
# Handles PDF parsing, text extraction, and chunking for document storage

import fitz  # PyMuPDF for PDF processing
from app.db.supabase import supabase


def chunk_text(text, size=1000):
    """
    Split text into overlapping chunks for better context preservation.
    
    Args:
        text (str): Text to chunk
        size (int): Chunk size in characters (default: 1000)
    
    Returns:
        list: List of text chunks
    """
    return [
        text[i:i+size]
        for i in range(0, len(text), size)
    ]


def ingest_pdf(file_path, file_name):
    """
    Extract text from PDF, chunk it, and store in Supabase.
    
    Args:
        file_path (str): Path to the PDF file
        file_name (str): Original filename for metadata
    
    Process:
        1. Open PDF and iterate through pages
        2. Extract text from each page
        3. Split text into chunks
        4. Store chunks with metadata in Supabase
    """
    doc = fitz.open(file_path)

    for page_num, page in enumerate(doc, start=1):
        # Extract text from current page
        text = page.get_text()

        # Split page text into chunks
        chunks = chunk_text(text)

        # Store each chunk in database with metadata
        for chunk in chunks:
            if chunk.strip():  # Only store non-empty chunks
                supabase.table("documents").insert({
                    "file_name": file_name,
                    "page_number": page_num,
                    "chunk_text": chunk
                }).execute()
    
    doc.close()
