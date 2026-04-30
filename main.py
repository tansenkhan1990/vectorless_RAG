# Vectorless RAG Application
# Production PDF Question-Answering System with Agentic AI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router

# Initialize FastAPI application
app = FastAPI(
    title="Production PDF Vectorless RAG",
    description="Retrieval-Augmented Generation system for intelligent PDF question-answering",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Vectorless RAG",
        "description": "Production PDF Question-Answering System",
        "docs": "/docs",
        "endpoints": {
            "upload_pdf": "POST /api/upload",
            "ask_question": "POST /api/chat"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔════════════════════════════════════════╗
    ║  Vectorless RAG Server Starting       ║
    ║  API Docs: http://localhost:8001/docs ║
    ╚════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
