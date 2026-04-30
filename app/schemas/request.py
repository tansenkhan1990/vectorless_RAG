# API Request Models
# Defines the structure of incoming API requests

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Chat request model for question-answering endpoint.
    
    Attributes:
        query (str): User's question about PDF documents
                    - Minimum 3 characters (single word too short)
                    - Maximum 300 characters (prevent abuse)
    
    Example:
        >>> req = ChatRequest(query="What is machine learning?")
        >>> req.query
        'What is machine learning?'
    """
    query: str = Field(
        ...,
        min_length=3,
        max_length=300,
        description="User question to answer from PDF documents"
    )
