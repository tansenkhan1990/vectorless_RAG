# Vectorless RAG: Production PDF Question-Answering System

A modern, production-ready Retrieval-Augmented Generation (RAG) system that enables intelligent question-answering over PDF documents using an agentic AI architecture. This system leverages **OpenAI Agents**, **LangGraph**, and **Supabase** to create a vectorless approach to document retrieval and analysis.

## 🚀 Features

- **PDF Upload & Ingestion**: Seamlessly upload and process PDF documents with automatic text extraction and chunking
- **Vectorless Retrieval**: Uses semantic search via Supabase RPC functions instead of traditional vector embeddings
- **Agentic AI**: Powered by OpenAI Agents for intelligent reasoning and accurate answers
- **LangGraph Workflow**: Orchestrates multi-step processes with document retrieval followed by answer generation
- **RESTful API**: Clean FastAPI endpoints for document upload and question answering
- **Source Tracking**: Returns source documents and page numbers for answer transparency
- **Local Model Support**: Configured to work with local models via Ollama for privacy and cost-effectiveness

## 📋 Project Overview

This is an **agentic AI system** that combines:
1. **Document Ingestion**: PDFs are uploaded, parsed, and chunked
2. **Semantic Retrieval**: Queries are matched against document chunks using Supabase search
3. **Agent-Based Answering**: OpenAI Agents generate answers based only on retrieved context
4. **Workflow Orchestration**: LangGraph manages the multi-step reasoning process

The system is designed to prevent hallucinations by:
- Only allowing agents to use provided PDF content
- Explicitly instructing agents to return "I don't know" when answers aren't found
- Tracking sources for every response

## 🏗️ Architecture

```
┌─────────────────┐
│  FastAPI Server │
└────────┬────────┘
         │
    ┌────┴──────┐
    │            │
┌───▼──────┐  ┌─▼────────────┐
│  Upload  │  │  Chat Query  │
│ Endpoint │  │   Endpoint   │
└───┬──────┘  └─┬────────────┘
    │          │
    │    ┌─────▼──────────┐
    │    │  LangGraph     │
    │    │  Workflow      │
    │    └─┬───────────┬──┘
    │      │           │
    │   ┌──▼──┐    ┌───▼────────┐
    │   │PDFIn│    │ Retrieval  │
    │   │gestor    │Node        │
    │   └──┬──┘    └───┬────────┘
    │      │           │
    │   ┌──▼──────────▼──┐
    │   │  Supabase DB   │
    │   └─────────────────┘
    │
    ├───────────────────────┐
    │                       │
    ▼                       ▼
┌─────────┐          ┌──────────────┐
│ Answer  │          │  Agent       │
│ Storage │          │  (OpenAI)    │
└─────────┘          └──────────────┘
```

## 📁 Project Structure

```
vectorless_RAG/
├── main.py                          # FastAPI application entry point
├── pyproject.toml                   # Project dependencies & metadata
├── requirements.txt                 # Additional requirements
├── .env                             # Environment variables (keep secret)
├── README.md                        # This file
├── app/
│   ├── agents/
│   │   └── answer_agent.py         # OpenAI Agent configuration for answering
│   ├── api/
│   │   ├── chat.py                 # Chat endpoint (query answering)
│   │   └── upload.py               # Upload endpoint (PDF processing)
│   ├── config/
│   │   └── settings.py             # Configuration settings (env vars)
│   ├── db/
│   │   ├── schema.sql              # Database schema
│   │   └── supabase.py             # Supabase client initialization
│   ├── graph/
│   │   └── workflow.py             # LangGraph workflow definition
│   ├── ingestion/
│   │   └── pdf_ingestor.py         # PDF parsing & chunking logic
│   ├── prompts/
│   │   └── templates.py            # Prompt templates for agent
│   ├── retrieval/
│   │   └── retriever.py            # Document retrieval from Supabase
│   └── schemas/
│       ├── request.py              # API request models
│       └── response.py             # API response models
├── uploads/                         # Temporary PDF upload directory
└── my_env/                          # Virtual environment

```

## 🔧 Prerequisites

- **Python 3.12+**
- **Ollama** (for local model inference) - Download from [ollama.ai](https://ollama.ai)
- **Supabase Account** - Free tier available at [supabase.com](https://supabase.com)
- **OpenAI API Key** (optional if using local models)
- **UV Package Manager** - Modern Python package manager

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
cd ~/Documents/learning/Agentic\ AI\ /Vectorless\ RAG/vectorless_RAG
```

### 2. Create Virtual Environment with UV

```bash
uv venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
uv add fastapi uvicorn openai openai-agents langgraph supabase python-dotenv pydantic pymupdf python-multipart
```

Or if `pyproject.toml` is already configured:

```bash
uv sync
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env  # If template exists
# Or manually create .env with:
```

**Required Variables:**

```env
# Local Model (Ollama)
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama

# Model Configuration
LOCAL_MODEL_NAME=qwen3-vl:235b-cloud          # Your Ollama model
LOCAL_EMBEDDING_MODEL=nomic-embed-text:latest # For embeddings

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_publishable_key_here

# OpenAI Agents Settings
OPENAI_AGENTS_DISABLE_TRACING=1
OPENAI_DISABLE_TELEMETRY=true
```

### 5. Start Ollama (if using local models)

```bash
ollama serve
```

In another terminal, pull your model:

```bash
ollama pull qwen3-vl:235b-cloud
ollama pull nomic-embed-text:latest
```

### 6. Initialize Supabase Database

Run the schema in `app/db/schema.sql` on your Supabase instance:

```sql
-- Create documents table
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  file_name TEXT NOT NULL,
  page_number INTEGER,
  chunk_text TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create search function (RPC)
CREATE OR REPLACE FUNCTION search_docs(
  search_query TEXT,
  match_count INT DEFAULT 5
)
RETURNS TABLE (
  file_name TEXT,
  page_number INTEGER,
  chunk_text TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    documents.file_name,
    documents.page_number,
    documents.chunk_text
  FROM documents
  WHERE documents.chunk_text ILIKE '%' || search_query || '%'
  LIMIT match_count;
END;
$$ LANGUAGE plpgsql;
```

## 🚀 Running the Application

### Start the Server

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run with uvicorn
uvicorn main:app --reload --port 8001
```

The API will be available at: **http://localhost:8001**

### FastAPI Documentation

- **Interactive Docs (Swagger UI)**: http://localhost:8001/docs
- **Alternative Docs (ReDoc)**: http://localhost:8001/redoc

## 📡 API Endpoints

### 1. Upload PDF Document

**Endpoint:** `POST /upload`

**Request:**
```bash
curl -X POST "http://localhost:8001/upload" \
  -F "file=@path/to/your/document.pdf"
```

**Response:**
```json
{
  "message": "Uploaded and indexed",
  "file": "document.pdf"
}
```

**What happens:**
1. PDF is validated (must be `.pdf` extension)
2. File is saved to `uploads/` directory
3. PDF is parsed page-by-page using PyMuPDF (fitz)
4. Text is extracted and split into 1000-character chunks
5. Chunks are stored in Supabase with file name and page number

### 2. Ask Questions

**Endpoint:** `POST /chat`

**Request:**
```bash
curl -X POST "http://localhost:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main findings?"
  }'
```

**Response:**
```json
{
  "answer": "The main findings are...",
  "sources": ["document.pdf"]
}
```

**What happens:**
1. Query is processed through LangGraph workflow
2. **Retrieve Node**: Searches Supabase for matching document chunks
3. **Answer Node**: Sends chunks + query to OpenAI Agent
4. Agent generates answer using only provided context
5. Response includes answer and source documents

## 🔄 How It Works: Step-by-Step

### Document Upload Flow

```
PDF Upload → File Saved → PDF Parsed → Text Extracted → 
Chunked (1000 chars) → Stored in Supabase
```

### Question-Answering Flow

```
User Query 
    ↓
LangGraph Workflow (graph/workflow.py)
    ├─ Retrieve Node
    │   └─ retrieve_docs(query) 
    │       └─ Supabase RPC: search_docs()
    │           └─ Returns 5 matching chunks
    │
    └─ Answer Node
        └─ build_prompt(query, docs)
            └─ OpenAI Agent processes prompt
                └─ Returns answer based on context only
                    └─ ChatResponse with answer + sources
```

### Core Components

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **PDF Ingestor** | Extract & chunk PDFs | PyMuPDF (fitz) |
| **Retriever** | Find relevant docs | Supabase RPC |
| **Agent** | Generate answers | OpenAI Agents |
| **Workflow** | Orchestrate steps | LangGraph |
| **API** | User interface | FastAPI |
| **Database** | Store documents | Supabase (PostgreSQL) |

## 🛠️ Configuration

### Model Selection

**For Local Models (Ollama):**
```env
OPENAI_BASE_URL=http://localhost:11434/v1
LOCAL_MODEL_NAME=qwen3-vl:235b-cloud
```

**For OpenAI API:**
```env
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-...
LOCAL_MODEL_NAME=gpt-4
```

### Chunk Size Adjustment

Edit `app/ingestion/pdf_ingestor.py`:
```python
def chunk_text(text, size=1000):  # Change size parameter
    return [text[i:i+size] for i in range(0, len(text), size)]
```

### Retrieval Limit

Edit `app/retrieval/retriever.py`:
```python
def retrieve_docs(query: str):
    result = supabase.rpc(
        "search_docs",
        {
            "search_query": query,
            "match_count": 5  # Change this number
        }
    ).execute()
    return result.data
```

## 🧠 Agent Instructions

The agent is configured in `app/agents/answer_agent.py`:

```python
answer_agent = Agent(
    name="PDFKnowledgeAgent",
    model=settings.MODEL,
    instructions="""
Answer only from provided PDF content.
Never hallucinate.
"""
)
```

Modify the `instructions` to change agent behavior.

## 🔒 Security & Best Practices

- ✅ `.env` file is in `.gitignore` (never commit secrets)
- ✅ Supabase credentials are kept in environment variables
- ✅ Agent is restricted to PDF content only
- ✅ Input validation on query length (3-300 chars)
- ✅ PDF file type validation on upload

## 🐛 Troubleshooting

### "Address already in use"
```bash
# Use a different port
uvicorn main:app --reload --port 8002
```

### "Could not import module"
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Try running from project root
cd /Users/tansenkhan/Documents/learning/Agentic\ AI\ /Vectorless\ RAG/vectorless_RAG
uvicorn main:app --reload
```

### Supabase Connection Error
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check that the `documents` table exists
- Ensure the `search_docs()` RPC function is created

### Ollama Connection Error
- Verify Ollama is running: `ollama serve`
- Check `OPENAI_BASE_URL=http://localhost:11434/v1`
- Verify model exists: `ollama list`

### No Results from Queries
- Ensure PDFs have been uploaded
- Check Supabase `documents` table has data
- Verify search query keywords match document content
- Try simpler, more specific queries

## 📊 Testing the System

### With cURL

```bash
# 1. Upload a PDF
curl -X POST "http://localhost:8001/upload" \
  -F "file=@sample.pdf"

# 2. Ask a question
curl -X POST "http://localhost:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the document about?"}'
```

### With Python

```python
import requests

# Upload
with open("sample.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8001/upload",
        files={"file": f}
    )
    print(response.json())

# Query
response = requests.post(
    "http://localhost:8001/chat",
    json={"query": "What is the main topic?"}
)
print(response.json())
```

## 🎓 Technologies Used

| Technology | Purpose | Version |
|-----------|---------|---------|
| **FastAPI** | Web framework | ≥0.136.1 |
| **LangGraph** | Workflow orchestration | ≥1.1.10 |
| **OpenAI Agents** | AI reasoning | ≥0.14.8 |
| **Supabase** | Database & search | ≥2.29.0 |
| **PyMuPDF** | PDF parsing | ≥1.27.2 |
| **Pydantic** | Data validation | ≥2.13.3 |
| **Python** | Runtime | ≥3.12 |

## 🚀 Future Enhancements

- [ ] **Hybrid Search**: Combine keyword search with vector embeddings
- [ ] **Multi-Modal PDFs**: Better handling of images and tables
- [ ] **Streaming Responses**: Real-time answer generation
- [ ] **Citation Links**: Direct links to source chunks
- [ ] **Query Expansion**: Improve search with query rephrasing
- [ ] **RAG Evaluation**: RAGAS metrics for quality assessment
- [ ] **Admin Dashboard**: Document management UI
- [ ] **Rate Limiting**: API usage controls
- [ ] **Authentication**: User accounts and permissions
- [ ] **Conversation History**: Multi-turn chat support

## 📝 Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `OPENAI_BASE_URL` | LLM API endpoint | `http://localhost:11434/v1` |
| `OPENAI_API_KEY` | API authentication | `ollama` or `sk-...` |
| `LOCAL_MODEL_NAME` | Model identifier | `qwen3-vl:235b-cloud` |
| `LOCAL_EMBEDDING_MODEL` | Embedding model | `nomic-embed-text:latest` |
| `SUPABASE_URL` | Database endpoint | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | Supabase API key | `sb_publishable_...` |

## 📄 License

This project is part of an AI learning initiative. Feel free to use, modify, and distribute as needed.

## 👨‍💻 Contributing

To improve this project:
1. Test thoroughly before committing
2. Follow Python PEP 8 style guide
3. Update documentation for new features
4. Keep `.env` and secrets out of git

---

**Built with ❤️ for Production PDF Question-Answering**