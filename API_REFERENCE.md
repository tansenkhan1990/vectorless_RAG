# API Reference

Complete API documentation for the Vectorless RAG system.

## Base URL

```
http://localhost:8001/api
```

## Authentication

Currently, the API has **no authentication**. In production, add API keys or JWT tokens.

## Response Format

All responses are JSON. Errors return appropriate HTTP status codes.

---

## Endpoints

### 1. Upload PDF Document

Upload a PDF file for ingestion and indexing.

**Endpoint:** `POST /upload`

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:**
  - `file` (file, required): PDF file to upload

**cURL Example:**
```bash
curl -X POST "http://localhost:8001/api/upload" \
  -F "file=@document.pdf"
```

**Python Example:**
```python
import requests

with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8001/api/upload",
        files={"file": f}
    )
    print(response.json())
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8001/api/upload', {
  method: 'POST',
  body: formData
})
.then(r => r.json())
.then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "message": "Uploaded and indexed successfully",
  "file": "document.pdf"
}
```

**Error Responses:**

```json
// 400 Bad Request - Wrong file type
{
  "detail": "Only PDF files are allowed"
}
```

```json
// 400 Bad Request - No file provided
{
  "detail": "Field required"
}
```

**Status Codes:**
- `200 OK` - File uploaded successfully
- `400 Bad Request` - Invalid file format
- `422 Unprocessable Entity` - Missing required field
- `500 Internal Server Error` - Server error during processing

**Processing Details:**
1. File is validated (must be `.pdf`)
2. File is saved to `uploads/` directory
3. PDF is parsed with PyMuPDF
4. Text is extracted page-by-page
5. Text is chunked into 1000-character segments
6. Chunks are stored in Supabase with metadata:
   - `file_name`: Original filename
   - `page_number`: Page number (1-indexed)
   - `chunk_text`: Text content
7. Full-text search index is updated

**Notes:**
- Maximum file size: No built-in limit (add if needed)
- Supported format: PDF only
- Processing time: Depends on PDF size (typically <30s)
- Duplicate files: Allowed (creates separate entries)

---

### 2. Ask Question

Ask a question about uploaded PDF documents.

**Endpoint:** `POST /chat`

**Request:**
- **Content-Type:** `application/json`
- **Body:** JSON object with:
  - `query` (string, required): Question to ask
    - Minimum length: 3 characters
    - Maximum length: 300 characters

**cURL Example:**
```bash
curl -X POST "http://localhost:8001/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main findings?"
  }'
```

**Python Example:**
```python
import requests

response = requests.post(
    "http://localhost:8001/api/chat",
    json={"query": "What is machine learning?"}
)
print(response.json())
```

**JavaScript Example:**
```javascript
fetch('http://localhost:8001/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'What is the main topic?'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "answer": "The main findings are that machine learning algorithms can improve accuracy by 45% when trained on larger datasets.",
  "sources": ["ML_guide.pdf"]
}
```

**Error Responses:**

```json
// 422 Unprocessable Entity - Query too short
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "query"],
      "msg": "String should have at least 3 characters",
      "input": "hi"
    }
  ]
}
```

```json
// 422 Unprocessable Entity - Query too long
{
  "detail": [
    {
      "type": "string_too_long",
      "loc": ["body", "query"],
      "msg": "String should have at most 300 characters",
      "input": "..."
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Question processed successfully
- `400 Bad Request` - Invalid request
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

**Processing Details:**
1. Query is validated (length 3-300 chars)
2. LangGraph workflow is invoked with query
3. **Retrieve Node:**
   - Searches Supabase with full-text search
   - Returns top 5 matching document chunks
   - Each chunk includes: file_name, page_number, chunk_text
4. **Answer Node:**
   - Builds structured prompt with chunks
   - Sends to OpenAI Agent
   - Agent generates answer based only on provided context
5. Response is formatted with:
   - `answer`: AI-generated response
   - `sources`: Unique PDF files used (deduplicated)

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | AI-generated answer to the question |
| `sources` | array[string] | List of PDF file names used for the answer |

**Query Guidelines:**

✅ **Good Queries:**
- "What is machine learning?"
- "List the main findings of this research"
- "How does the algorithm work?"
- "What are the limitations discussed?"

❌ **Poor Queries:**
- "ok" (too short)
- "Lorem ipsum dolor sit amet..." (over 300 chars)
- Empty string (validation error)
- Special characters only (may not match documents)

**Answer Behavior:**
- If information is found: Returns answer with sources
- If information not found: Returns "I don't know"
- Never hallucinated or inferred information
- Always grounded in provided document chunks

**Notes:**
- Response time: 2-5 seconds (depends on model)
- Results are not cached (each query is fresh)
- Sources are deduplicated
- Answer quality depends on document relevance
- Agent instructions can be customized

---

### 3. API Information

Get API metadata and available endpoints.

**Endpoint:** `GET /`

**cURL Example:**
```bash
curl "http://localhost:8001/api"
```

**Response (200 OK):**
```json
{
  "name": "Vectorless RAG",
  "description": "Production PDF Question-Answering System",
  "docs": "/docs",
  "endpoints": {
    "upload_pdf": "POST /api/upload",
    "ask_question": "POST /api/chat"
  }
}
```

---

### 4. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /health`

**cURL Example:**
```bash
curl "http://localhost:8001/api/health"
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI (Recommended):** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

You can test all endpoints directly from the browser!

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid file format |
| 422 | Unprocessable Entity | Query validation failed |
| 500 | Internal Server Error | Database connection error |

### Error Response Format

```json
{
  "detail": "Error description here"
}
```

Or with validation details:

```json
{
  "detail": [
    {
      "type": "error_type",
      "loc": ["field_name"],
      "msg": "Error message",
      "input": "value_provided"
    }
  ]
}
```

### Common Error Scenarios

**PDF Upload Errors:**

```bash
# ❌ Wrong file format
curl -X POST http://localhost:8001/api/upload -F "file=@doc.txt"
# Response: 400 - Only PDF files are allowed

# ❌ No file provided
curl -X POST http://localhost:8001/api/upload
# Response: 422 - Field required
```

**Query Errors:**

```bash
# ❌ Query too short
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hi"}'
# Response: 422 - String should have at least 3 characters

# ❌ Query too long
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "...[over 300 chars]..."}'
# Response: 422 - String should have at most 300 characters

# ❌ Missing query field
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{}'
# Response: 422 - Field required
```

---

## Data Models

### ChatRequest

Request body for chat endpoint.

```python
{
  "query": "string"  # Length: 3-300 characters
}
```

**Example:**
```json
{
  "query": "What is the main topic of this document?"
}
```

### ChatResponse

Response body for chat endpoint.

```python
{
  "answer": "string",      # AI-generated answer
  "sources": ["string"]    # PDF file names
}
```

**Example:**
```json
{
  "answer": "The main topic is artificial intelligence and its applications in healthcare.",
  "sources": ["AI_in_healthcare.pdf", "Medical_AI.pdf"]
}
```

### Upload Response

Response body for upload endpoint.

```python
{
  "message": "string",  # Status message
  "file": "string"      # Uploaded filename
}
```

**Example:**
```json
{
  "message": "Uploaded and indexed successfully",
  "file": "research_paper.pdf"
}
```

---

## Rate Limiting

Currently **no rate limiting** is implemented. For production:

```python
# Add to main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("30/minute")
def chat(req: ChatRequest):
    # ... implementation
```

---

## Authentication

Currently **no authentication** required. For production, implement:

```python
# Using API Keys
from fastapi import Header, HTTPException

async def verify_api_key(x_token: str = Header(...)):
    if x_token != "expected_key":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_token

# Using JWT
from fastapi_jwt_auth import AuthJWT

@app.post("/chat")
def chat(req: ChatRequest, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    # ... implementation
```

---

## Performance Tips

### Optimize Queries

```bash
# ✓ Specific, targeted questions
"What are the main results in section 3?"

# ✗ Vague, broad questions
"Tell me everything"
```

### Batch Operations

```python
# Instead of uploading one file at a time
files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
for file in files:
    upload_pdf(file)
```

### Caching Considerations

Responses are not cached. For frequently asked questions, implement caching:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_chat(query: str):
    # ... implementation
```

---

## Pagination (Future Enhancement)

For large result sets, pagination may be added:

```bash
GET /api/search?query=topic&page=1&limit=10
```

---

## Webhooks (Future Enhancement)

Future versions may support webhooks for async processing:

```python
POST /api/webhooks/upload
{
  "callback_url": "https://example.com/callback",
  "file": "document.pdf"
}
```

---

## Versioning

Current API version: **0.1.0**

Future: Support `Accept-Version` header or URL versioning:
- `/api/v1/chat`
- `/api/v2/chat`

---

## CORS Configuration

Currently allows all origins. For production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

---

## Testing the API

### cURL Collection

```bash
# Upload a PDF
curl -X POST http://localhost:8001/api/upload \
  -F "file=@sample.pdf"

# Ask a question
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this about?"}'

# Check health
curl http://localhost:8001/api/health

# Get API info
curl http://localhost:8001/
```

### Postman Collection

Import this JSON into Postman:

```json
{
  "info": {"name": "Vectorless RAG API"},
  "item": [
    {
      "name": "Upload PDF",
      "request": {
        "method": "POST",
        "url": "http://localhost:8001/api/upload"
      }
    },
    {
      "name": "Chat",
      "request": {
        "method": "POST",
        "url": "http://localhost:8001/api/chat",
        "body": {
          "mode": "raw",
          "raw": "{\"query\": \"What is this?\"}"
        }
      }
    }
  ]
}
```

---

## Support

For issues or questions:
1. Check [GETTING_STARTED.md](GETTING_STARTED.md)
2. Review [README.md](README.md)
3. Check [DEVELOPMENT.md](DEVELOPMENT.md)
4. Visit interactive docs: http://localhost:8001/docs

---

**Last Updated:** April 2026
