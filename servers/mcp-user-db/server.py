from tools import mcp_tools_users
from mcp.server.fastmcp import FastMCP
from config import get_conn, close_conn

server = FastMCP(description="Create, list and get users from SQLite DB", host="0.0.0.0", port=8002)

@server.on_event("startup")
async def startup():
    """Inicializa a conexão com o banco de dados no início."""
    server.state.db = await get_conn()

@server.on_event("shutdown")
async def shutdown():
    """Fecha a conexão com o banco de dados no final."""
    if hasattr(server.state, "db"):
        await close_conn(server.state.db)

for tool in mcp_tools_users:
    server.tool()(tool)


if __name__ == "__main__":
    server.run(transport="sse")