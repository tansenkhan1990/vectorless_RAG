from agents import Agent
from app.config.settings import settings

# Initialize the PDF Knowledge Agent
# This agent is configured to answer questions based only on provided PDF content
answer_agent = Agent(
    name="PDFKnowledgeAgent",
    model=settings.MODEL,
    instructions="""
Answer only from provided PDF content.
Never hallucinate.
If the answer is not found in the provided context, say "I don't know."
Be precise and cite specific information from the documents.
"""
)