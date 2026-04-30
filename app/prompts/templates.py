# Prompt Templates Module
# Defines the prompt structure for the OpenAI Agent

def build_prompt(query: str, docs: list) -> str:
    """
    Build a structured prompt for the OpenAI Agent.
    
    This prompt template ensures the agent:
    1. Only uses provided document context
    2. Returns "I don't know" when information is missing
    3. Provides accurate, grounded answers
    
    Args:
        query (str): User's question
        docs (list): Retrieved document chunks with metadata
    
    Returns:
        str: Formatted prompt ready for agent processing
    
    Example:
        >>> docs = [
        ...     {"file_name": "doc.pdf", "page_number": 1, "chunk_text": "..."},
        ...     {"file_name": "doc.pdf", "page_number": 2, "chunk_text": "..."}
        ... ]
        >>> prompt = build_prompt("What is X?", docs)
    """
    # Format document context with source information
    context = "\n\n".join([
        f"{d['file_name']} page {d['page_number']}:\n{d['chunk_text']}"
        for d in docs
    ])

    # Structured prompt with clear instructions
    return f"""
Use ONLY the context below to answer the question.

If the answer is not found in the context, respond with:
I don't know.

Do NOT make up or infer information beyond what is provided.

Context:
{context}

Question:
{query}

Answer:
"""
