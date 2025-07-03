from typing import Optional, Dict, Any, List
from pydantic import Field
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.tags_api import TagsApi
from config import configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datadog Tags Service")

@mcp.tool()
def list_host_tags(
    source: Optional[str] = Field(default=None, description="Source of the tags (e.g., 'chef', 'aws')")
) -> Dict[str, Any]:
    """List tags for all hosts.

    Args:
        source (Optional[str], optional): Source of the tags (e.g., 'chef', 'aws').
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): List of host tags if successful"""
    try:
        with ApiClient(configuration) as api_client:
            tags_api = TagsApi(api_client)
            response = tags_api.list_host_tags(source=source)
            return {"status": "success", "message": "Host tags listed successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error listing host tags: {e}"}

@mcp.tool()
def add_host_tags(
    host_name: str = Field(..., description="The name of the host"),
    tags: List[str] = Field(..., description="The tags to add"),
    source: Optional[str] = Field(default=None, description="Source of the tags (e.g., 'chef', 'aws')")
) -> Dict[str, Any]:
    """Add tags to a specific host.

    Args:
        host_name (str): The name of the host.
        tags (List[str]): The tags to add.
        source (Optional[str], optional): Source of the tags (e.g., 'chef', 'aws').
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            tags_api = TagsApi(api_client)
            tags_api.create_host_tags(host_name, body={"tags": tags}, source=source)
            return {"status": "success", "message": "Tags added to host successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error adding tags to host: {e}"}

@mcp.tool()
def delete_host_tags(
    host_name: str = Field(..., description="The name of the host"),
    source: Optional[str] = Field(default=None, description="Source of the tags (e.g., 'chef', 'aws')")
) -> Dict[str, Any]:
    """Delete all tags from a specific host.

    Args:
        host_name (str): The name of the host.
        source (Optional[str], optional): Source of the tags (e.g., 'chef', 'aws').
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            tags_api = TagsApi(api_client)
            tags_api.delete_host_tags(host_name, source=source)
            return {"status": "success", "message": "Tags deleted from host successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error deleting tags from host: {e}"}
