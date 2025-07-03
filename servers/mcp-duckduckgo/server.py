from tools import mcp_duckduckgo_tools
from mcp.server.fastmcp import FastMCP

server = FastMCP(description="Duckduckgo Search", host="0.0.0.0", port=8000)

for tool in mcp_duckduckgo_tools:
    server.tool()(tool)


if __name__ == "__main__":
    server.run(transport="sse")