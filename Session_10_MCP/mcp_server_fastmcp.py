# Works with fastmcp >= 2.0 (my version is 2.12.5)

from fastmcp import FastMCP
import pandas as pd

# Load your dataset
df = pd.read_csv("data.csv")

# Create MCP server instance
app = FastMCP("sales_data_mcp")

@app.tool()     #app.tool() decorator
def summarize() -> dict:
    """Return dataset summary information."""
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "numeric_stats": df.describe(include="all").fillna("").to_dict(),
    }

@app.tool()
def query(expr: str) -> dict:
    """Filter rows using pandas.query syntax."""
    try:
        result = df.query(expr)
    except Exception as e:
        return {"error": str(e)}
    return {"count": len(result), "rows": result.head(10).to_dict(orient="records")}

if __name__ == "__main__":
    app.run()
