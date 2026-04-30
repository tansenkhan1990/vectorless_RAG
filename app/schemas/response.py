# API Response Models
# Defines the structure of API responses

from pydantic import BaseModel


class ChatResponse(BaseModel):
    """
    Chat response model for question-answering endpoint.
    
    Attributes:
        answer (str): AI-generated answer to the user's question
                     - Based only on provided PDF context
                     - Returns "I don't know" if answer not found
        sources (list[str]): List of PDF file names used for the answer
    
    Example:
        >>> resp = ChatResponse(
        ...     answer="Machine learning is...",
        ...     sources=["ML_guide.pdf"]
        ... )
        >>> resp.answer
        'Machine learning is...'
        >>> resp.sources
        ['ML_guide.pdf']
    """
    answer: str
    sources: list[str]
