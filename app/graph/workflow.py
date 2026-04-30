# LangGraph Workflow Module
# Orchestrates the RAG pipeline: retrieval -> answer generation

from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.retrieval.retriever import retrieve_docs
from app.prompts.templates import build_prompt
from app.agents.answer_agent import answer_agent


class State(TypedDict):
    """
    Workflow state that flows through the graph nodes.
    
    Attributes:
        query (str): User's question
        docs (list): Retrieved document chunks
        answer (str): Generated answer from agent
    """
    query: str
    docs: list
    answer: str


def retrieve_node(state: State) -> dict:
    """
    First node: Retrieve relevant documents.
    
    Takes the user's query and searches Supabase for matching document chunks.
    
    Args:
        state (State): Current workflow state with query
    
    Returns:
        dict: Updated state with retrieved documents
    """
    docs = retrieve_docs(state["query"])
    return {"docs": docs}


def answer_node(state: State) -> dict:
    """
    Second node: Generate answer using agent.
    
    Builds a prompt with retrieved documents and query, then uses
    the OpenAI Agent to generate an answer based only on provided context.
    
    Args:
        state (State): Current workflow state with query and docs
    
    Returns:
        dict: Updated state with generated answer
    """
    prompt = build_prompt(
        state["query"],
        state["docs"]
    )

    result = answer_agent.run(prompt)

    return {"answer": result.final_output}


# Build the workflow graph
builder = StateGraph(State)

# Add nodes
builder.add_node("retrieve", retrieve_node)
builder.add_node("answer", answer_node)

# Define flow: retrieve -> answer -> end
builder.set_entry_point("retrieve")
builder.add_edge("retrieve", "answer")
builder.add_edge("answer", END)

# Compile graph into executable workflow
graph = builder.compile()
