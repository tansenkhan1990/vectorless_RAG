from app.db.supabase import supabase


def retrieve_docs(query: str):
    result = supabase.rpc(
        "search_docs",
        {
            "search_query": query,
            "match_count": 5
        }
    ).execute()

    return result.data