from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from fastmcp import Client
from fastmcp.client import PythonStdioTransport
import asyncio

# -------------------------------
# LLM
# -------------------------------
# --- Load API Key ---
from dotenv import load_dotenv
import os

load_dotenv(override=True, dotenv_path="../.env")
my_api_key = os.getenv("OPENAI_API_KEY")

# Choose the OpenAI LLM
llm = ChatOpenAI(
 
    model="gpt-5-nano",
    openai_api_key=my_api_key
)
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -------------------------------
# Graph State
# -------------------------------
class GraphState(TypedDict):
    user_input: str
    intent: str
    result: dict
    answer: str

# -------------------------------
# Router Node
# -------------------------------
async def route_intent(state: GraphState):
    prompt = f"""
        You are an AI assistant for Antela.ai.

        Classify the user request into ONE intent:
        - overview
        - comps

        User request:
        {state['user_input']}
        """

    response = llm.invoke([HumanMessage(content=prompt)])
    intent = response.content.lower()

    if "comp" in intent:
        return {"intent": "comps"}
    return {"intent": "overview"}

# -------------------------------
# Market Overview Node
# -------------------------------
async def market_snapshot(state: GraphState):
    transport = PythonStdioTransport("mcp_server_fastmcp.py")
    async with Client(transport) as client:
        result = await client.call_tool("summarize", {})
    return {"result": result}

# -------------------------------
# Comps Node
# -------------------------------
async def find_comps(state: GraphState):
    expr_prompt = f"""
Convert the user request into a pandas.query expression.

User request:
{state['user_input']}
"""

    expr = llm.invoke([HumanMessage(content=expr_prompt)]).content

    transport = PythonStdioTransport("mcp_server_fastmcp.py")
    async with Client(transport) as client:
        result = await client.call_tool("query", {"expr": expr})

    return {"result": result}

# -------------------------------
# Final Answer Node
# -------------------------------
async def final_answer(state: GraphState):
    answer_prompt = f"""
    You are an Antela.ai AI assistant.

    User asked:
    {state['user_input']}

    Tool result:
    {state['result']}

    Respond in clear, business-friendly language.
    """

    answer = llm.invoke([HumanMessage(content=answer_prompt)]).content
    return {"answer": answer}

# -------------------------------
# Build Graph
# -------------------------------
graph = StateGraph(GraphState)

graph.add_node("router", route_intent)
graph.add_node("overview_node", market_snapshot)
graph.add_node("comps_node", find_comps)
graph.add_node("final", final_answer)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    lambda s: s["intent"],
    {
        "overview": "overview_node",
        "comps": "comps_node",
    }
)

graph.add_edge("overview_node", "final")
graph.add_edge("comps_node", "final")
graph.add_edge("final", END)

app = graph.compile()

# -------------------------------
# Run (Async Entry Point)
# -------------------------------
async def main():
    while True:
        user_input = input("\nAsk Antela AI (or 'exit'): ")
        if user_input.lower() == "exit":
            break

        result = await app.ainvoke({"user_input": user_input})
        print("\nAI Answer:\n", result["answer"])

if __name__ == "__main__":
    asyncio.run(main())
