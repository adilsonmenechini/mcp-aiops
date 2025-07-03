from typing import Optional, Dict, Any
from pydantic import Field
from datadog_api_client import ApiClient
from datadog_api_client.v2.api.roles_api import RolesApi
from config import configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datadog Roles Service")

@mcp.tool()
def list_roles() -> Dict[str, Any]:
    """List all roles.

    Args:
        None

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): List of roles if successful"""
    try:
        with ApiClient(configuration) as api_client:
            roles_api = RolesApi(api_client)
            response = roles_api.list_roles()
            return {"status": "success", "message": "Roles listed successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error listing roles: {e}"}

@mcp.tool()
def get_role(
    role_id: str = Field(..., description="The ID of the role to retrieve")
) -> Dict[str, Any]:
    """Get details of a specific role.

    Args:
        role_id (str): The ID of the role to retrieve.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Role details if successful"""
    try:
        with ApiClient(configuration) as api_client:
            roles_api = RolesApi(api_client)
            response = roles_api.get_role(role_id)
            return {"status": "success", "message": "Role retrieved successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error retrieving role: {e}"}

@mcp.tool()
def create_role(
    name: str = Field(..., description="The name of the role"),
    description: Optional[str] = Field(default=None, description="A description of the role")
) -> Dict[str, Any]:
    """Create a new role.

    Args:
        name (str): The name of the role.
        description (Optional[str], optional): A description of the role.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Created role data if successful"""
    try:
        with ApiClient(configuration) as api_client:
            roles_api = RolesApi(api_client)
            body = {"data": {"type": "roles", "attributes": {"name": name, "description": description}}}
            response = roles_api.create_role(body=body)
            return {"status": "success", "message": "Role created successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error creating role: {e}"}

@mcp.tool()
def delete_role(
    role_id: str = Field(..., description="The ID of the role to delete")
) -> Dict[str, Any]:
    """Delete a specific role.

    Args:
        role_id (str): The ID of the role to delete.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            roles_api = RolesApi(api_client)
            roles_api.delete_role(role_id)
            return {"status": "success", "message": "Role deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error deleting role: {e}"}

@mcp.tool()
def update_role(
    role_id: str = Field(..., description="The ID of the role to update"),
    name: Optional[str] = Field(default=None, description="The new name of the role"),
    description: Optional[str] = Field(default=None, description="The new description of the role")
) -> Dict[str, Any]:
    """Update a specific role.

    Args:
        role_id (str): The ID of the role to update.
        name (Optional[str], optional): The new name of the role.
        description (Optional[str], optional): The new description of the role.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Updated role data if successful"""
    try:
        with ApiClient(configuration) as api_client:
            roles_api = RolesApi(api_client)
            body = {"data": {"type": "roles", "id": role_id, "attributes": {}}}
            if name:
                body["data"]["attributes"]["name"] = name
            if description:
                body["data"]["attributes"]["description"] = description
            response = roles_api.update_role(role_id, body=body)
            return {"status": "success", "message": "Role updated successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error updating role: {e}"}
