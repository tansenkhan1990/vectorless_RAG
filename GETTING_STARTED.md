# Getting Started with Vectorless RAG

Quick start guide to set up and run the Vectorless RAG system.

## 🎯 5-Minute Setup

### 1. Prerequisites Check

```bash
# Check Python version (needs 3.12+)
python3 --version

# Check if Ollama is installed
ollama --version

# Or download from https://ollama.ai
```

### 2. Clone & Navigate

```bash
cd ~/Documents/learning/Agentic\ AI\ /Vectorless\ RAG/vectorless_RAG
```

### 3. Set Up Virtual Environment

```bash
# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
```

### 4. Install Dependencies

```bash
# Using the pre-configured pyproject.toml
uv sync

# OR install packages directly
uv add fastapi uvicorn openai openai-agents langgraph supabase python-dotenv pydantic pymupdf python-multipart
```

### 5. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env and fill in:
# - Your Supabase URL and Key
# - Model name (qwen3-vl:235b-cloud for local)
```

### 6. Start Ollama (Local Models)

```bash
# In one terminal
ollama serve

# In another terminal, pull the model
ollama pull qwen3-vl:235b-cloud
ollama pull nomic-embed-text:latest
```

### 7. Start the Server

```bash
# Make sure virtual environment is active
source .venv/bin/activate

# Run the server
uvicorn main:app --reload --port 8001
```

You should see:
```
╔════════════════════════════════════════╗
║  Vectorless RAG Server Starting       ║
║  API Docs: http://localhost:8001/docs ║
╚════════════════════════════════════════╝
```

## 🧪 Test the System

### Using FastAPI Docs (Recommended)

1. Open http://localhost:8001/docs in your browser
2. Click on `POST /api/upload`
3. Upload a PDF file
4. Click on `POST /api/chat`
5. Ask a question about your PDF

### Using cURL

```bash
# Upload a PDF
curl -X POST "http://localhost:8001/upload" \
  -F "file=@your_document.pdf"

# Ask a question
curl -X POST "http://localhost:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic?"}'
```

### Using Python

```python
import requests

# Upload
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8001/api/upload",
        files={"file": f}
    )
    print(response.json())

# Query
response = requests.post(
    "http://localhost:8001/api/chat",
    json={"query": "What is this document about?"}
)
print(response.json())
```

## 📁 Project Structure Quick Reference

```
├── main.py                  # FastAPI app entry point
├── .env                     # Your configuration (keep secret!)
├── .env.example             # Template for environment variables
├── app/
│   ├── agents/              # AI agent configuration
│   ├── api/                 # REST endpoints
│   ├── config/              # Settings and configuration
│   ├── db/                  # Database connection & schema
│   ├── graph/               # LangGraph workflow
│   ├── ingestion/           # PDF processing
│   ├── prompts/             # Prompt templates
│   ├── retrieval/           # Document search
│   └── schemas/             # Request/response models
└── uploads/                 # Temporary PDF storage
```

## 🔗 Key Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/upload` | Upload PDF document |
| POST | `/api/chat` | Ask question about PDFs |
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API documentation |

## ⚙️ Configuration Guide

### Using Local Models (Ollama)

In `.env`:
```env
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
LOCAL_MODEL_NAME=qwen3-vl:235b-cloud
```

### Using OpenAI API

In `.env`:
```env
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-key-here
LOCAL_MODEL_NAME=gpt-4
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --reload --port 8002
```

### Supabase Connection Failed
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check that the documents table exists
- Ensure the `search_docs()` function is created in Supabase

### Module Import Error
```bash
# Reinstall dependencies
uv sync --force

# Or manually install
uv add -r requirements.txt
```

### Ollama Connection Failed
```bash
# Start Ollama
ollama serve

# In another terminal, test connection
curl http://localhost:11434/api/tags
```

## 📚 Next Steps

1. **Read the README.md** for comprehensive documentation
2. **Explore the API docs** at http://localhost:8001/docs
3. **Upload test PDFs** to populate the database
4. **Ask questions** and observe the answers
5. **Customize agent instructions** in `app/agents/answer_agent.py`

## 💡 Tips & Tricks

- **Create a `.gitignore` entry** for uploads: Add `uploads/*` to `.gitignore`
- **Use sample PDFs** to test before using your own documents
- **Monitor logs** to see the workflow in action
- **Adjust chunk size** in `app/ingestion/pdf_ingestor.py` for better results
- **Modify agent instructions** for different behavior

## 📖 Documentation

- **Main README**: See [README.md](README.md) for full documentation
- **API Docs**: Visit http://localhost:8001/docs when server is running
- **Architecture**: Check [README.md#🏗️-architecture](README.md#-architecture)

## 🆘 Need Help?

Check these resources:
1. **README.md** - Full project documentation
2. **Code comments** - Each file has detailed docstrings
3. **FastAPI Docs** - http://localhost:8001/docs (interactive)
4. **Environment variables** - See `.env.example`

---

**Ready to ask questions? Upload a PDF and get started!** 🚀
