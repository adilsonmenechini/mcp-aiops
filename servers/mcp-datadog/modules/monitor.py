from typing import Optional, List, Dict, Any
from pydantic import Field
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from config import configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datadog Monitor Service")

@mcp.tool()
def create_monitor(
    name: str = Field(..., description="The name of the monitor"),
    type: str = Field(..., description="The type of the monitor (e.g., 'metric alert')"),
    query: str = Field(..., description="The query to evaluate for the monitor"),
    message: Optional[str] = Field(default=None, description="The message to include with notifications"),
    tags: Optional[List[str]] = Field(default=None, description="A list of tags to associate with the monitor")
) -> Dict[str, Any]:
    """Create a new monitor.

    Args:
        name (str): The name of the monitor.
        type (str): The type of the monitor (e.g., 'metric alert').
        query (str): The query to evaluate for the monitor.
        message (Optional[str], optional): The message to include with notifications.
        tags (Optional[List[str]], optional): A list of tags to associate with the monitor.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Created monitor data if successful"""
    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            body = {
                "name": name,
                "type": type,
                "query": query,
                "message": message,
                "tags": tags or []
            }
            response = monitors_api.create_monitor(body=body)
            return {"status": "success", "message": "Monitor created successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error creating monitor: {e}"}

@mcp.tool()
def delete_monitor(
    monitor_id: int = Field(..., description="The ID of the monitor to delete")
) -> Dict[str, Any]:
    """Delete a specific monitor.

    Args:
        monitor_id (int): The ID of the monitor to delete.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            monitors_api.delete_monitor(monitor_id)
            return {"status": "success", "message": "Monitor deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error deleting monitor: {e}"}

@mcp.tool()
def get_monitor_status(
    name: Optional[str] = Field(default="", description="The name of the monitor to filter"),
    group_states: Optional[List[str]] = Field(default=None, description="Filter by group states (e.g., 'alert', 'warn')"),
    tags: Optional[List[str]] = Field(default=None, description="Filter by tags")
) -> Dict[str, Any]:
    """Fetch the status of Datadog monitors.

    Args:
        name (Optional[str], optional): The name of the monitor to filter.
        group_states (Optional[List[str]], optional): Filter by group states (e.g., 'alert', 'warn').
        tags (Optional[List[str]], optional): Filter by tags.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Contains monitor list and status summary
                - monitors (list): List of monitor objects with details
                - summary (dict): Count of monitors by status"""
    group_states = group_states or []
    tags = tags or []

    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            response = monitors_api.list_monitors(
                group_states=','.join(group_states) if group_states else None,
                name=','.join(name) if name else None,
                tags=','.join(tags) if tags else None
            )

            if not response:
                return {"status": "error", "message": "No monitor data returned", "content": []}

            monitors_data = [
                {
                    "name": monitor.name or "",
                    "id": monitor.id or 0,
                    "status": str(monitor.overall_state).lower() if monitor.overall_state else "unknown",
                    "message": monitor.message,
                    "tags": monitor.tags or [],
                    "query": monitor.query or "",
                    "last_updated_ts": int(monitor.modified.timestamp()) if monitor.modified else None,
                }
                for monitor in response
            ]

            summary = {status: 0 for status in ["alert", "warn", "no_data", "ok", "ignored", "skipped", "unknown"]}
            for monitor in response:
                status = str(monitor.overall_state).lower() if monitor.overall_state else "unknown"
                summary[status] = summary.get(status, 0) + 1

            return {
                "status": "success",
                "message": "Monitors retrieved successfully",
                "content": {
                    "monitors": monitors_data,
                    "summary": summary
                }
            }
    except Exception as e:
        return {"status": "error", "message": f"Error fetching monitor status: {e}", "content": []}

@mcp.tool()
def update_monitor(
    monitor_id: int = Field(..., description="The ID of the monitor to update"),
    name: Optional[str] = Field(default=None, description="The new name of the monitor"),
    query: Optional[str] = Field(default=None, description="The new query for the monitor"),
    message: Optional[str] = Field(default=None, description="The new message for the monitor"),
    tags: Optional[List[str]] = Field(default=None, description="The new tags for the monitor")
) -> Dict[str, Any]:
    """Update an existing monitor.

    Args:
        monitor_id (int): The ID of the monitor to update.
        name (Optional[str], optional): The new name of the monitor.
        query (Optional[str], optional): The new query for the monitor.
        message (Optional[str], optional): The new message for the monitor.
        tags (Optional[List[str]], optional): The new tags for the monitor.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Updated monitor data if successful"""
    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            body = {}
            if name:
                body["name"] = name
            if query:
                body["query"] = query
            if message:
                body["message"] = message
            if tags:
                body["tags"] = tags
            response = monitors_api.update_monitor(monitor_id, body=body)
            return {"status": "success", "message": "Monitor updated successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error updating monitor: {e}"}

@mcp.tool()
def create_monitor_config_policy(
    name: str = Field(..., description="The name of the monitor config policy"),
    policy_type: str = Field(..., description="The type of the policy (e.g., 'tag')"),
    tags: List[str] = Field(..., description="The tags to apply the policy to"),
    policy: Dict[str, Any] = Field(..., description="The policy configuration")
) -> Dict[str, Any]:
    """Create a new monitor configuration policy.

    Args:
        name (str): The name of the monitor config policy.
        policy_type (str): The type of the policy (e.g., 'tag').
        tags (List[str]): The tags to apply the policy to.
        policy (Dict[str, Any]): The policy configuration.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Created policy data if successful"""
    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            body = {
                "data": {
                    "type": "monitor_config_policy",
                    "attributes": {
                        "name": name,
                        "policy_type": policy_type,
                        "tags": tags,
                        "policy": policy,
                    },
                }
            }
            response = monitors_api.create_monitor_config_policy(body=body)
            return {"status": "success", "message": "Monitor config policy created successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error creating monitor config policy: {e}"}

@mcp.tool()
def update_monitor_config_policy(
    policy_id: str = Field(..., description="The ID of the monitor config policy to update"),
    name: Optional[str] = Field(default=None, description="The new name of the policy"),
    policy: Optional[Dict[str, Any]] = Field(default=None, description="The updated policy configuration")
) -> Dict[str, Any]:
    """Update an existing monitor configuration policy.

    Args:
        policy_id (str): The ID of the monitor config policy to update.
        name (Optional[str], optional): The new name of the policy.
        policy (Optional[Dict[str, Any]], optional): The updated policy configuration.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Updated policy data if successful"""
    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            body = {"data": {"type": "monitor_config_policy", "id": policy_id, "attributes": {}}}
            if name:
                body["data"]["attributes"]["name"] = name
            if policy:
                body["data"]["attributes"]["policy"] = policy
            response = monitors_api.update_monitor_config_policy(policy_id, body=body)
            return {"status": "success", "message": "Monitor config policy updated successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error updating monitor config policy: {e}"}

@mcp.tool()
def delete_monitor_config_policy(
    policy_id: str = Field(..., description="The ID of the monitor config policy to delete")
) -> Dict[str, Any]:
    """Delete a monitor configuration policy.

    Args:
        policy_id (str): The ID of the monitor config policy to delete.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            monitors_api.delete_monitor_config_policy(policy_id)
            return {"status": "success", "message": "Monitor config policy deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error deleting monitor config policy: {e}"}

@mcp.tool()
def list_monitor_config_policies() -> Dict[str, Any]:
    """List all monitor configuration policies.

    Args:
        None

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): List of monitor configuration policies if successful"""
    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            response = monitors_api.list_monitor_config_policies()
            return {"status": "success", "message": "Monitor config policies retrieved successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error listing monitor config policies: {e}"}

@mcp.tool()
def search_monitors(
    query: str = Field(..., description="The search query for monitors"),
    page: int = Field(default=0, description="Page number for pagination"),
    per_page: int = Field(default=30, description="Number of monitors per page")
) -> Dict[str, Any]:
    """Search monitors using a query.

    Args:
        query (str): The search query for monitors.
        page (int, optional): Page number for pagination. Defaults to 0.
        per_page (int, optional): Number of monitors per page. Defaults to 30.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Search results if successful"""
    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            response = monitors_api.search_monitors(query=query, page=page, per_page=per_page)
            return {"status": "success", "message": "Monitors retrieved successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error searching monitors: {e}"}

@mcp.tool()
def get_monitor(
    monitor_id: int = Field(..., description="The ID of the monitor to retrieve")
) -> Dict[str, Any]:
    """Retrieve details of a specific monitor.

    Args:
        monitor_id (int): The ID of the monitor to retrieve.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Monitor details if successful"""
    try:
        with ApiClient(configuration) as api_client:
            monitors_api = MonitorsApi(api_client)
            response = monitors_api.get_monitor(monitor_id)
            return {"status": "success", "message": "Monitor retrieved successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error retrieving monitor: {e}"}
