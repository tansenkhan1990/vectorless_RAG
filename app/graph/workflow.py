from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.retrieval.retriever import retrieve_docs
from app.prompts.templates import build_prompt
from app.agents.answer_agent import answer_agent


class State(TypedDict):
    query: str
    docs: list
    answer: str


def retrieve_node(state):
    docs = retrieve_docs(state["query"])
    return {"docs": docs}


def answer_node(state):
    prompt = build_prompt(
        state["query"],
        state["docs"]
    )

    result = answer_agent.run(prompt)

    return {"answer": result.final_output}


builder = StateGraph(State)

builder.add_node("retrieve", retrieve_node)
builder.add_node("answer", answer_node)

builder.set_entry_point("retrieve")

builder.add_edge("retrieve", "answer")
builder.add_edge("answer", END)

graph = builder.compile()