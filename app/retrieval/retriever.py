# Document Retrieval Module
# Handles semantic search and retrieval of relevant document chunks

from app.db.supabase import supabase


def retrieve_docs(query: str, match_count: int = 5):
    """
    Search for relevant document chunks based on query.
    
    This function uses Supabase's full-text search RPC to find documents
    matching the user's query. Results are ranked by relevance.
    
    Args:
        query (str): The search query
        match_count (int): Number of results to return (default: 5)
    
    Returns:
        list: List of document chunks with metadata:
            - file_name: Name of the PDF
            - page_number: Page number in PDF
            - chunk_text: The actual text content
    
    Example:
        >>> docs = retrieve_docs("What is machine learning?")
        >>> len(docs)
        5
        >>> docs[0]["file_name"]
        'AI_guide.pdf'
    """
    result = supabase.rpc(
        "search_docs",
        {
            "search_query": query,
            "match_count": match_count
        }
    ).execute()

    return result.data
