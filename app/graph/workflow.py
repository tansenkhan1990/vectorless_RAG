# Workflow Module
# Runs the Agent pipeline using OpenAI Agents SDK Runner

from agents import Runner
from app.agents.answer_agent import answer_agent


def run_query(query: str) -> dict:
    """
    Run a user query through the PDF Knowledge Agent.

    The agent will:
    1. Use its retrieve_docs tool to search Supabase
    2. Analyze the retrieved context
    3. Generate a grounded answer

    Args:
        query (str): User's question about uploaded PDF documents

    Returns:
        dict: Result with keys:
            - answer (str): The agent's answer
            - sources (list[str]): Source PDF filenames used
    """
    result = Runner.run_sync(answer_agent, query)

    # Extract source filenames from tool call results
    sources = _extract_sources(result)

    return {
        "answer": result.final_output,
        "sources": sources
    }


def _extract_sources(result) -> list[str]:
    """
    Extract unique source PDF filenames from the agent's tool calls.

    Parses the raw_responses to find retrieve_docs tool outputs
    and extracts [Source: filename, Page N] patterns.

    Args:
        result: RunResult from the Agent runner

    Returns:
        list[str]: Unique PDF filenames referenced in the answer
    """
    import re

    sources = set()

    # Walk through all items in the run to find tool outputs
    for item in result.new_items:
        # Check for tool output items
        if hasattr(item, 'output') and isinstance(item.output, str):
            # Extract filenames from [Source: filename, Page N] pattern
            matches = re.findall(
                r'\[Source:\s*(.+?),\s*Page\s*\d+\]',
                item.output
            )
            sources.update(matches)

    return list(sources)
