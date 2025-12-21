from fastmcp import FastMCP
import asyncio
from backend_langgraph_flow import app

mcp = FastMCP("market_ai")

@mcp.tool()
def ask_market_ai(user_input: str) -> dict:
    """
    Entry point for all market questions.
    """
    result = asyncio.run(
        app.ainvoke({"user_input": user_input})
    )
    return {
        "answer": result["answer"]
    }

if __name__ == "__main__":
    mcp.run()
