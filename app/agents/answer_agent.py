# PDF Knowledge Agent
# Uses OpenAI Agents SDK with retrieval tool for RAG

from agents import Agent
from app.config.settings import settings
from app.retrieval.retriever import retrieve_docs

# Initialize the PDF Knowledge Agent with retrieval tool
# The agent autonomously decides when to search documents
answer_agent = Agent(
    name="PDFKnowledgeAgent",
    model=settings.MODEL,
    instructions="""
You are a PDF Knowledge Agent. Your job is to answer user questions 
based ONLY on content from uploaded PDF documents.

Rules:
1. ALWAYS use the retrieve_docs tool first to search for relevant content.
2. Answer ONLY from the retrieved document context.
3. Never hallucinate or make up information.
4. If no relevant content is found, respond with: "I don't know."
5. Be precise and cite the source file name and page number.
6. Keep answers clear and well-structured.
""",
    tools=[retrieve_docs],
)