from typing import List, Dict, Any
from pydantic import Field
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.service_checks_api import ServiceChecksApi
from config import configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datadog Service Checks Service")

@mcp.tool()
def submit_service_check(
    check_name: str = Field(..., description="The name of the service check"),
    host_name: str = Field(..., description="The name of the host"),
    status: int = Field(..., description="The status of the service check (e.g., 0 for OK, 1 for WARNING, etc.)"),
    message: str = Field(default="", description="A message describing the service check status"),
    tags: List[str] = Field(default_factory=list, description="Tags to associate with the service check")
) -> Dict[str, Any]:
    """Submit a service check.

    Args:
        check_name (str): The name of the service check.
        host_name (str): The name of the host.
        status (int): The status of the service check (e.g., 0 for OK, 1 for WARNING, etc.).
        message (str, optional): A message describing the service check status. Defaults to "".
        tags (List[str], optional): Tags to associate with the service check. Defaults to empty list.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            service_checks_api = ServiceChecksApi(api_client)
            body = [{"check": check_name, "host_name": host_name, "status": status, "message": message, "tags": tags}]
            service_checks_api.submit_service_check(body=body)
            return {"status": "success", "message": "Service check submitted successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error submitting service check: {e}"}

@mcp.tool()
def list_service_checks() -> Dict[str, Any]:
    """List all available service checks.

    Args:
        None

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): List of service checks if successful"""
    try:
        with ApiClient(configuration) as api_client:
            service_checks_api = ServiceChecksApi(api_client)
            response = service_checks_api.list_service_checks()
            return {"status": "success", "message": "Service checks listed successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error listing service checks: {e}"}
