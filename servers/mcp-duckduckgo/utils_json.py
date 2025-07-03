def format_success_result(items: list) -> dict:
    return {
        "jsonrpc": "2.0",
        "result": {
            "status": "success",
            "items": items
        }
    }

def format_error_result(message: str) -> dict:
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": -32000,
            "message": message
        }
    }

def format_results_list(results: list) -> list:
    """
    Formata os resultados do duckduckgo-search (dicionários) e inclui o raw_result.
    """
    formatted = []
    for idx, item in enumerate(results):
        try:
            formatted.append({
                "id": str(idx + 1),
                "title": item.get("title", "Sem título").strip(),
                "url": item.get("href", "URL não disponível").strip(),
                "snippet": item.get("body", "Conteúdo não disponível").strip(),
                "raw_result": item
            })
        except Exception as e:
            formatted.append({
                "id": str(idx + 1),
                "title": "Erro no item",
                "url": "",
                "snippet": f"Erro ao processar resultado: {str(e)}",
                "raw_result": {}
            })
    return formatted
