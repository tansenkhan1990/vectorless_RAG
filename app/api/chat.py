# Chat API Endpoint
# Handles question-answering over uploaded PDF documents

from fastapi import APIRouter
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse
from app.graph.workflow import run_query

router = APIRouter(tags=["Question Answering"])


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Ask a question about uploaded PDF documents.

    This endpoint processes user queries through the Agent RAG pipeline:
    1. Agent uses retrieve_docs tool to search Supabase
    2. Agent analyzes retrieved document context
    3. Agent generates answer based only on provided context
    4. Returns answer with source documents

    Args:
        req (ChatRequest): Query request containing the question

    Returns:
        ChatResponse: Answer and source document names

    Example:
        ```bash
        curl -X POST "http://localhost:8001/api/chat" \\
          -H "Content-Type: application/json" \\
          -d '{
            "query": "What are the main findings?"
          }'
        ```

    Response:
        ```json
        {
          "answer": "The main findings are...",
          "sources": ["document.pdf"]
        }
        ```

    Notes:
        - Query must be between 3-300 characters
        - Agent will only use provided document context
        - Returns "I don't know" if answer not found
        - Sources list shows which PDFs were used
    """
    result = run_query(req.query)

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"]
    )
