import json
import sys
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.hosts_api import HostsApi
from config import configuration
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("Datadog Host Service")




@mcp.tool()
def list_hosts(
    filter: str = Field(default="", description="Filter hosts by name, alias, or tag"),
    sort_field: str = Field(default=None, description="Field to sort results by"),
    sort_dir: str = Field(default=None, description="Sort direction: 'asc' or 'desc'"),
    count: int = Field(default=10, ge=1, le=1000, description="Max number of hosts to return (default: 10)")
) -> dict:
    """Retrieves all hosts from Datadog.
    
    Args:
        filter (str, optional): Filter hosts by name, alias, or tag. Defaults to "".
        sort_field (str, optional): Field to sort results by.
        sort_dir (str, optional): Sort direction: 'asc' or 'desc'.
        count (int, optional): Max number of hosts to return (1-1000). Defaults to 10.
    
    Returns:
        dict: A dictionary containing:
            - content (list): List of host objects with name, id, mute status, last reported time, up status, and URL
            - error (str): Error message if the operation fails"""
    try:
        with ApiClient(configuration) as api_client:
            hosts_api = HostsApi(api_client)
            kwargs = {"count": count}
            if filter:
                kwargs["filter"] = filter
            if sort_field:
                kwargs["sort_field"] = sort_field
            if sort_dir:
                kwargs["sort_dir"] = sort_dir
            
            response = hosts_api.list_hosts(**kwargs)
            
            if response is not None and response.host_list is not None:
                hosts = [
                    {
                        "name": host.name,
                        "id": host.id,
                        "mute": host.is_muted,
                        "last_reported": host.last_reported_time,
                        "up": host.up,
                        "url": f"https://app.datadoghq.com/infrastructure?host={host.name}",
                    }
                    for host in response.host_list
                ]

                result = {
                    "content": hosts
                }
                
                return result
            else:
                return {"error": "Invalid response from Datadog API."}
    except Exception as e:
        return {"error": f"Error fetching hosts: {e}"}

@mcp.tool()
def get_host_totals() -> dict:
    """Gets the total number of active hosts.
    
    Args:
        None
    
    Returns:
        dict: A dictionary containing:
            - content (list): List with a single text element containing JSON response with host totals
                - type (str): Type of content ('text')
                - text (str): JSON string with host totals data or error message"""
    try:
        with ApiClient(configuration) as api_client:
            hosts_api = HostsApi(api_client)
            response = hosts_api.get_host_totals()
            return {"content": [{"type": "text", "text": json.dumps(response.to_dict(), indent=2)}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error fetching host totals: {e}"}]}

@mcp.tool()
def mute_host(host_name: str, message: str = "Muted via MCP") -> dict:
    """Mutes a specific host.
    
    Args:
        host_name (str): The name of the host to mute.
        message (str, optional): Message explaining why the host was muted. Defaults to "Muted via MCP".
    
    Returns:
        dict: A dictionary containing:
            - content (list): List with a single text element containing JSON response
                - type (str): Type of content ('text')
                - text (str): JSON string with mute operation result or error message"""
    try:
        with ApiClient(configuration) as api_client:
            hosts_api = HostsApi(api_client)
            settings = HostMuteSettings(message=message)
            response = hosts_api.mute_host(host_name, body=settings)
            return {"content": [{"type": "text", "text": json.dumps(response.to_dict(), indent=2)}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error muting host: {e}"}]}

@mcp.tool()
def unmute_host(host_name: str) -> dict:
    """Unmutes a specific host.
    
    Args:
        host_name (str): The name of the host to unmute.
    
    Returns:
        dict: A dictionary containing:
            - content (list): List with a single text element containing JSON response
                - type (str): Type of content ('text')
                - text (str): JSON string with unmute operation result or error message"""
    try:
        with ApiClient(configuration) as api_client:
            hosts_api = HostsApi(api_client)
            response = hosts_api.unmute_host(host_name)
            return {"content": [{"type": "text", "text": json.dumps(response.to_dict(), indent=2)}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error unmuting host: {e}"}]}

