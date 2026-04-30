from agents import Agent
from app.config.settings import settings

answer_agent = Agent(
    name="PDFKnowledgeAgent",
    model=settings.MODEL,
    instructions="""
Answer only from provided PDF content.
Never hallucinate.
"""
)