from typing import Dict, Any, Optional
from pydantic import Field
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.usage_metering_api import UsageMeteringApi
from config import configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datadog Usage Service")

@mcp.tool()
def get_hourly_usage(
    start_date: str = Field(..., description="The start date for hourly usage in YYYY-MM-DD format"),
    end_date: str = Field(..., description="The end date for hourly usage in YYYY-MM-DD format"),
    usage_type: Optional[str] = Field(default=None, description="The type of usage to retrieve (e.g., 'logs', 'hosts')")
) -> Dict[str, Any]:
    """Retrieve hourly usage data.

    Args:
        start_date (str): The start date for hourly usage in YYYY-MM-DD format.
        end_date (str): The end date for hourly usage in YYYY-MM-DD format.
        usage_type (Optional[str], optional): The type of usage to retrieve (e.g., 'logs', 'hosts').
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Hourly usage data if successful"""
    try:
        with ApiClient(configuration) as api_client:
            usage_api = UsageMeteringApi(api_client)
            response = usage_api.get_hourly_usage(start_date=start_date, end_date=end_date, usage_type=usage_type)
            return {"status": "success", "message": "Hourly usage retrieved successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error retrieving hourly usage: {e}"}
