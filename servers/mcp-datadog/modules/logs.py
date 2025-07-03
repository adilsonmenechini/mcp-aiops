from typing import Optional, Dict, Any
from pydantic import Field
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.logs_api import LogsApi
from config import configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datadog Logs Service")

@mcp.tool()
def archive_logs(
    query: str = Field(..., description="The query to filter logs for archiving"),
    start: str = Field(..., description="Start time in ISO8601 format"),
    end: str = Field(..., description="End time in ISO8601 format")
) -> Dict[str, Any]:
    """Archive logs based on a query.
    
    Args:
        query (str): The query to filter logs for archiving.
        start (str): Start time in ISO8601 format.
        end (str): End time in ISO8601 format.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Archive operation response data if successful"""
    try:
        with ApiClient(configuration) as api_client:
            logs_api = LogsApi(api_client)
            body = {"query": query, "from": start, "to": end}
            response = logs_api.archive_logs(body=body)
            return {"status": "success", "message": "Logs archived successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error archiving logs: {e}"}
