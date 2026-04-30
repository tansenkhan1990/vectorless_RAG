# Development Guide

Comprehensive guide for developers working on the Vectorless RAG project.

## 📚 Architecture Overview

The system follows a modular, production-ready architecture:

```
┌─────────────────┐
│   FastAPI App   │ main.py
└────────┬────────┘
         │
    ┌────┴──────────┬──────────────┐
    │               │              │
┌───▼──────┐   ┌────▼────┐   ┌─────▼────┐
│  Upload  │   │  Chat   │   │ Schemas  │
│  Router  │   │  Router │   │ &Models  │
└───┬──────┘   └────┬────┘   └─────────┘
    │               │
    │          ┌────▼──────────────────┐
    │          │   LangGraph Workflow   │
    │          │   (graph/workflow.py)  │
    │          └─┬──────────────────┬──┘
    │            │                  │
    │         ┌──▼──┐          ┌────▼────────┐
    │         │Retrieve      │Answer       │
    │         │Node         │Node         │
    │         └──┬──┘        └────┬────────┘
    │            │                │
    ├────────────┼────────────────┘
    │            │
    │    ┌───────▼──────────┐
    │    │   Supabase DB    │
    │    │ (PostgreSQL)     │
    │    └──────────────────┘
    │
    └────────────────┬──────────────┐
                     │              │
            ┌────────▼──────┐  ┌────▼──────┐
            │ PDF Ingestor  │  │ Retriever  │
            │ (fitz/pymupdf)│  │ (RPC)      │
            └───────────────┘  └────────────┘
```

## 🗂️ Module Breakdown

### Core Modules

#### `app/agents/answer_agent.py`
- **Purpose**: OpenAI Agent configuration
- **Key Function**: Creates the agent that generates answers
- **Customization**: Modify `instructions` to change agent behavior
- **Tech**: openai-agents library

#### `app/api/upload.py`
- **Purpose**: PDF upload endpoint
- **Endpoint**: `POST /api/upload`
- **Process**: File validation → Save → Ingest → Index
- **Tech**: FastAPI, file handling

#### `app/api/chat.py`
- **Purpose**: Question answering endpoint
- **Endpoint**: `POST /api/chat`
- **Process**: Retrieve docs → Build prompt → Generate answer
- **Tech**: FastAPI, LangGraph

#### `app/db/supabase.py`
- **Purpose**: Database connection
- **Responsibility**: Initialize Supabase client
- **Usage**: All database operations go through this module
- **Tech**: supabase-py

#### `app/graph/workflow.py`
- **Purpose**: Workflow orchestration
- **Key Components**: StateGraph, retrieve_node, answer_node
- **Flow**: User query → Retrieve → Answer → Response
- **Tech**: LangGraph, TypedDict

#### `app/ingestion/pdf_ingestor.py`
- **Purpose**: PDF processing pipeline
- **Process**: Open PDF → Extract text → Chunk → Store
- **Customization**: Adjust chunk_text(size=1000) for different chunk sizes
- **Tech**: PyMuPDF (fitz)

#### `app/retrieval/retriever.py`
- **Purpose**: Document search and retrieval
- **Method**: Supabase RPC full-text search
- **Returns**: Top 5 matching document chunks by default
- **Tech**: Supabase RPC

#### `app/prompts/templates.py`
- **Purpose**: Prompt engineering
- **Role**: Format context + query for the agent
- **Customization**: Modify the system prompt here
- **Tech**: String templates

#### `app/config/settings.py`
- **Purpose**: Configuration management
- **Source**: Environment variables via python-dotenv
- **Validation**: Optional validation of required settings
- **Tech**: python-dotenv, os module

#### `app/schemas/request.py` & `response.py`
- **Purpose**: Request/response validation and documentation
- **Tech**: Pydantic v2
- **Features**: Automatic OpenAPI schema generation, validation

## 🔄 Data Flow

### Upload Flow

```
User Upload PDF
    ↓
FastAPI validates file extension (.pdf)
    ↓
Save file to uploads/ directory
    ↓
PDF Ingestor reads file with PyMuPDF
    ↓
For each page:
  - Extract text
  - Split into 1000-char chunks
  - Store in Supabase with metadata
    (file_name, page_number, chunk_text)
    ↓
Supabase triggers TSVector update
(for full-text search indexing)
    ↓
Return success response
```

### Question-Answering Flow

```
User Query (3-300 chars)
    ↓
LangGraph Workflow Invoked
    ↓
1. RETRIEVE NODE
   - Calls retrieve_docs(query)
   - Supabase RPC: search_docs()
   - Full-text search on TSVector
   - Returns top 5 chunks with metadata
    ↓
2. ANSWER NODE
   - Builds prompt with chunks
   - Passes to OpenAI Agent
   - Agent processes with instructions:
     * Use ONLY provided context
     * Return "I don't know" if no answer
   - Extracts final_output
    ↓
State becomes:
  {
    query: str,
    docs: list,
    answer: str
  }
    ↓
ChatResponse returns:
  {
    answer: str,
    sources: list[str]  # Unique file names
  }
```

## 🛠️ Development Workflow

### Setting Up Development Environment

```bash
# Create virtual environment
uv venv

# Activate
source .venv/bin/activate

# Install development dependencies
uv sync

# Or add dev tools manually
uv add --group dev pytest pytest-asyncio black flake8 mypy
```

### Code Style

Follow Python PEP 8:
```bash
# Format code
black app/

# Check linting
flake8 app/

# Type checking
mypy app/
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_retriever.py
```

## 🔧 Customization Guide

### Change Agent Behavior

Edit `app/agents/answer_agent.py`:
```python
answer_agent = Agent(
    name="CustomAgent",
    model=settings.MODEL,
    instructions="""
Your custom instructions here.
Define how agent should behave.
What constraints it should follow.
"""
)
```

### Adjust Chunk Size

Edit `app/ingestion/pdf_ingestor.py`:
```python
def chunk_text(text, size=2000):  # Increase or decrease
    return [text[i:i+size] for i in range(0, len(text), size)]
```

### Change Retrieval Strategy

Edit `app/retrieval/retriever.py`:
```python
def retrieve_docs(query: str, match_count: int = 10):  # Change from 5 to 10
    # ... implementation
```

### Modify Workflow Steps

Edit `app/graph/workflow.py`:
```python
# Add new nodes
builder.add_node("validate", validate_node)

# Add new edges
builder.add_edge("retrieve", "validate")
builder.add_edge("validate", "answer")
```

### Update Prompts

Edit `app/prompts/templates.py`:
```python
def build_prompt(query: str, docs: list) -> str:
    # Customize the prompt structure
    return f"""
Your custom prompt format here...
"""
```

## 🧪 Testing Strategies

### Unit Test Example

```python
# tests/test_retriever.py
from app.retrieval.retriever import retrieve_docs
from unittest.mock import patch

def test_retrieve_docs():
    query = "What is machine learning?"
    
    with patch('app.retrieval.retriever.supabase') as mock_db:
        mock_db.rpc.return_value.execute.return_value.data = [
            {"file_name": "test.pdf", "page_number": 1, "chunk_text": "ML is..."}
        ]
        
        results = retrieve_docs(query)
        assert len(results) == 1
        assert results[0]["file_name"] == "test.pdf"
```

### Integration Test Example

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_endpoint():
    with open("test.pdf", "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": f}
        )
    assert response.status_code == 200
    assert "file" in response.json()

def test_chat_endpoint():
    response = client.post(
        "/api/chat",
        json={"query": "What is this?"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()
```

## 📊 Performance Optimization

### Database Optimization

```sql
-- Already in schema.sql, but verify exists:

-- Full-text search index on chunk_text
CREATE INDEX idx_docs_search ON documents USING gin(tsv);

-- Faster page lookup
CREATE INDEX idx_docs_page ON documents(file_name, page_number);
```

### API Optimization

```python
# Add pagination for large result sets
def retrieve_docs(query: str, match_count: int = 5, offset: int = 0):
    result = supabase.rpc(
        "search_docs",
        {
            "search_query": query,
            "match_count": match_count,
            "offset": offset
        }
    ).execute()
    return result.data
```

### Caching

```python
# Add response caching
from functools import lru_cache

@lru_cache(maxsize=128)
def get_documents_cache(query: str):
    return retrieve_docs(query)
```

## 🔒 Security Considerations

### Secrets Management

```python
# ✓ DO: Use environment variables
api_key = os.getenv("OPENAI_API_KEY")

# ✗ DON'T: Hardcode secrets
api_key = "sk-1234567890"
```

### Input Validation

```python
# ✓ Already done with Pydantic
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=300)

# This prevents injection attacks and malformed requests
```

### CORS Security

```python
# Current: allows all origins (development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✗ For production, restrict this
)

# Production should be:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

## 🚀 Deployment Checklist

- [ ] Update `.env` with production secrets
- [ ] Set `OPENAI_BASE_URL` to production API
- [ ] Verify Supabase backups are enabled
- [ ] Enable HTTPS on FastAPI
- [ ] Restrict CORS to specific domains
- [ ] Set up monitoring/logging
- [ ] Add rate limiting
- [ ] Enable database read replicas
- [ ] Test error handling
- [ ] Set up CI/CD pipeline

## 📝 Code Standards

### Docstrings

```python
def retrieve_docs(query: str) -> list:
    """
    One-line summary.
    
    Longer description if needed.
    
    Args:
        query (str): Description
    
    Returns:
        list: Description
    
    Raises:
        ValueError: When...
    
    Example:
        >>> docs = retrieve_docs("What is AI?")
    """
```

### Type Hints

```python
# ✓ DO: Use type hints
def process_file(path: str) -> dict:
    pass

# ✗ DON'T: Skip type hints
def process_file(path):
    pass
```

### Error Handling

```python
# ✓ DO: Handle specific exceptions
try:
    result = supabase.table("documents").select("*").execute()
except Exception as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Database error")

# ✗ DON'T: Bare except
try:
    result = supabase.table("documents").select("*").execute()
except:
    pass
```

## 📚 Adding New Features

### Template: Adding a New API Endpoint

1. **Create schema** in `app/schemas/request.py` or `response.py`
2. **Create router** in `app/api/new_endpoint.py`
3. **Register router** in `main.py`
4. **Test endpoint** with FastAPI docs or cURL

### Template: Adding a Workflow Node

1. **Define node function** in `app/graph/workflow.py`
2. **Add to graph**: `builder.add_node("name", node_func)`
3. **Connect edges**: `builder.add_edge("prev", "new")`
4. **Test workflow** with sample data

### Template: Adding a Database Operation

1. **Write function** in appropriate `app/db/` module
2. **Use supabase client**: `supabase.table(...).method(...).execute()`
3. **Handle errors** gracefully
4. **Test with Supabase Studio**

## 🐛 Debugging Tips

### Enable Detailed Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Starting retrieval...")
logger.info("Retrieved 5 documents")
logger.error("Database connection failed")
```

### Debug the Workflow

```python
# Add print statements or use debugger
def answer_node(state):
    print(f"Query: {state['query']}")
    print(f"Retrieved docs: {len(state['docs'])}")
    
    prompt = build_prompt(state["query"], state["docs"])
    print(f"Prompt length: {len(prompt)}")
    
    result = answer_agent.run(prompt)
    return {"answer": result.final_output}
```

### Test Individual Components

```python
# Test retriever
from app.retrieval.retriever import retrieve_docs
docs = retrieve_docs("test query")
print(docs)

# Test agent
from app.agents.answer_agent import answer_agent
result = answer_agent.run("Test prompt")
print(result.final_output)
```

## 🔗 Dependencies

See `pyproject.toml` for complete list:

- **FastAPI**: Web framework
- **LangGraph**: Workflow orchestration
- **OpenAI Agents**: AI reasoning
- **Supabase**: Database
- **PyMuPDF**: PDF processing
- **Pydantic**: Data validation

## 📖 Additional Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [OpenAI Agents](https://platform.openai.com/docs/guides/agents)
- [Supabase Docs](https://supabase.com/docs)
- [PyMuPDF Docs](https://pymupdf.readthedocs.io/)

---

**Happy developing!** 🚀
