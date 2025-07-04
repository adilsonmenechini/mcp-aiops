# Módulos MCP DuckDuckGo

Este documento descreve os módulos disponíveis no servidor MCP DuckDuckGo e suas respectivas funcionalidades.

## Ferramentas

- **search**: Realiza uma busca no DuckDuckGo e retorna uma lista de resultados.
  - `query` (str): O termo a ser buscado.
  - `max_results` (int, opcional): Número máximo de resultados (padrão: 10).

- **fetch_content**: Extrai o conteúdo textual de uma URL.
  - `url` (str): A URL da página para extrair o conteúdo.