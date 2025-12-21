from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import pandas as pd
import os
from dotenv import load_dotenv

# ---------------------------
# Environment / LLM
# ---------------------------
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# ---------------------------
# Load Dataset
# ---------------------------
df = pd.read_csv("data.csv")

# ---------------------------
# Graph State
# ---------------------------
class GraphState(TypedDict):
    user_input: str
    intent: str
    query_expr: str
    result: dict
    answer: str
    error: str

# ---------------------------
# Intent Router
# ---------------------------
def classify_intent(state: GraphState):
    prompt = f"""
Classify the user request into one intent:
- overview
- comps

User request:
{state['user_input']}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    intent = response.content.lower()

    if "comp" in intent or "find" in intent:
        return {"intent": "comps"}
    return {"intent": "overview"}

# ---------------------------
# Market Overview Node
# ---------------------------
def market_overview(state: GraphState):
    summary = {
        "rows": len(df),
        "columns": list(df.columns),
        "stats": df.describe(include="all").fillna("").to_dict()
    }
    return {"result": summary}

# ---------------------------
# Comps Query Builder
# ---------------------------
def build_query(state: GraphState):
    prompt = f"""
Convert the user request into a valid pandas.query expression.

User request:
{state['user_input']}
"""
    expr = llm.invoke([HumanMessage(content=prompt)]).content
    return {"query_expr": expr}

# ---------------------------
# Execute Query
# ---------------------------
def run_query(state: GraphState):
    try:
        result = df.query(state["query_expr"])
        if len(result) == 0:
            return {"error": "No results found"}
        return {
            "result": result.head(10).to_dict(orient="records")
        }
    except Exception as e:
        return {"error": str(e)}

# ---------------------------
# Final Answer
# ---------------------------
def finalize(state: GraphState):
    prompt = f"""
User asked:
{state['user_input']}

Result:
{state.get('result')}

Error (if any):
{state.get('error')}

Respond clearly and concisely.
"""
    answer = llm.invoke([HumanMessage(content=prompt)]).content
    return {"answer": answer}

# ---------------------------
# Build Graph
# ---------------------------
graph = StateGraph(GraphState)

graph.add_node("router", classify_intent)
graph.add_node("overview", market_overview)
graph.add_node("build_query", build_query)
graph.add_node("run_query", run_query)
graph.add_node("final", finalize)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    lambda s: s["intent"],
    {
        "overview": "overview",
        "comps": "build_query"
    }
)

graph.add_edge("build_query", "run_query")
graph.add_edge("run_query", "final")
graph.add_edge("overview", "final")
graph.add_edge("final", END)

app = graph.compile()
