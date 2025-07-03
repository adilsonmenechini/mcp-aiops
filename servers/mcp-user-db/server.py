from tools import mcp_tools_users
from mcp.server.fastmcp import FastMCP

server = FastMCP(description="Create, list and get users from SQLite DB", host="0.0.0.0", port=8100)

for tool in mcp_tools_users:
    server.tool()(tool)


if __name__ == "__main__":
    server.run(transport="sse")