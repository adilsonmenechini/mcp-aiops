from tools import mcp_duckduckgo_tools
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.resources import FileResource
from pathlib import Path

server = FastMCP(description="Duckduckgo Search", host="0.0.0.0", port=8000)

for tool in mcp_duckduckgo_tools:
    server.tool()(tool)

@server.resource("docs://modules")
def view_documentation():
    """
    Retorna um link para a documentação deste serviço MCP.
    """
    readme_path = Path(__file__).parent / "docs/modules.md"
    if readme_path.exists():
        return FileResource(
            uri=f"file://{readme_path.resolve().as_posix()}",
            path=readme_path,
            name="modules.md",
            description="The project's modules.",
            mime_type="text/markdown"
        )

if __name__ == "__main__":
    server.run(transport="sse")