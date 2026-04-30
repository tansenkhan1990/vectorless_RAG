# Document Retrieval Tool
# Registered as an Agent function_tool for semantic search over Supabase

from agents import function_tool
from app.db.supabase import supabase


@function_tool
def retrieve_docs(query: str, match_count: int = 5) -> str:
    """
    Search for relevant PDF document chunks based on query.

    This tool searches Supabase using full-text search to find document
    chunks matching the user's question. Results are ranked by relevance.

    Args:
        query: The search query to find relevant document chunks.
        match_count: Number of results to return (default: 5).

    Returns:
        Formatted string of matching document chunks with source metadata.
    """
    result = supabase.rpc(
        "search_docs",
        {
            "search_query": query,
            "match_count": match_count
        }
    ).execute()

    docs = result.data

    if not docs:
        return "No relevant documents found."

    # Format results so the agent sees structured context
    formatted = []
    for d in docs:
        formatted.append(
            f"[Source: {d['file_name']}, Page {d['page_number']}]\n{d['chunk_text']}"
        )

    return "\n\n---\n\n".join(formatted)
