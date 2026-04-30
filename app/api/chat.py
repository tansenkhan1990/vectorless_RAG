from fastapi import APIRouter
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse
from app.graph.workflow import graph

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = graph.invoke({
        "query": req.query
    })

    return ChatResponse(
        answer=result["answer"],
        sources=list(set([
            d["file_name"]
            for d in result["docs"]
        ]))
    )