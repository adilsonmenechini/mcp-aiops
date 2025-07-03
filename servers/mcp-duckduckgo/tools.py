from mcp.server.fastmcp import Context, FastMCP
import json
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import httpx
import sys
import traceback
from utils_json import format_success_result, format_error_result, format_results_list

mcp = FastMCP()

@mcp.tool()
async def search(query: str, ctx: Context, max_results: int = 10) -> dict:
    """
    Busca informações no DuckDuckGo usando a lib duckduckgo-search.

    Args:
        query (str): A consulta de busca.
        max_results (int, optional): O número máximo de resultados a serem retornados. Default é 10.

    Returns:
        dict: Um dicionário contendo os resultados formatados.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        items = format_results_list(results)
        return {
            "result": json.dumps(format_success_result(items))
        }
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return {
            "result": json.dumps(format_error_result(f"Erro ao buscar: {str(e)}"))
        }

@mcp.tool()
async def fetch_content(url: str, ctx: Context) -> dict:
    """
    Recupera e extrai o conteúdo textual de uma URL.

    Args:
        url (str): A URL a ser acessada.

    Returns:
        dict: Um dicionário contendo o conteúdo textual formatado.
    """
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code} ao acessar {url}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove tags indesejadas
        for tag in soup(["script", "style", "noscript", "svg", "footer", "header", "form"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        # Limitar para evitar overload de tokens
        max_chars = 8000
        trimmed_text = text[:max_chars]

        return {
            "result": json.dumps(format_success_result([
                {
                    "id": "1",
                    "content": trimmed_text
                }
            ]))
        }

    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return {
            "result": json.dumps(format_error_result(f"Erro ao buscar conteúdo: {str(e)}"))
        }

mcp_duckduckgo_tools = (
    search,
    fetch_content
)