# Works with fastmcp >= 2.0 (my version is 2.12.5)

# pip install fastmcp
# pip install fastmcp>=2.0 langgraph langchain langchain-openai pandas python-dotenv

# cd Session_10_MCP
# python mcp_server_fastmcp.py

from fastmcp import FastMCP
import pandas as pd

df = pd.read_csv("data.csv")

app = FastMCP("antela_market_mcp")

@app.tool()
def summarize() -> dict:
    """Return CRE market dataset summary."""
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "numeric_stats": df.describe(include="all").fillna("").to_dict(),
    }

@app.tool()
def query(expr: str) -> dict:
    """Find comparable CRE properties using pandas.query."""
    try:
        result = df.query(expr)
    except Exception as e:
        return {"error": str(e)}

    return {
        "count": len(result),
        "rows": result.head(10).to_dict(orient="records")
    }

if __name__ == "__main__":
    app.run()
