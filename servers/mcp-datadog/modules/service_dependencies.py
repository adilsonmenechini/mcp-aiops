from typing import Optional, Dict, Any
from pydantic import Field
from datadog_api_client import ApiClient
from datadog_api_client.v2.api.service_dependencies_api import ServiceDependenciesApi
from config import configuration
from mcp.server.fastmcp import FastMCP
from datadog_api_client.exceptions import (
    ApiException
)

mcp = FastMCP("Datadog Service Dependencies Service")

@mcp.tool()
def list_service_dependencies(
    service_id: str = Field(..., description="The ID of the service to retrieve dependencies for")
) -> Dict[str, Any]:
    """List all dependencies for a specific service.

    Args:
        service_id (str): The ID of the service to retrieve dependencies for.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): List of service dependencies if successful"""
    try:
        with ApiClient(configuration) as api_client:
            service_dependencies_api = ServiceDependenciesApi(api_client)
            response = service_dependencies_api.list_service_dependencies(service_id)
            return {"status": "success", "message": "Service dependencies retrieved successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while retrieving service dependencies: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while retrieving service dependencies: {e}"}

@mcp.tool()
def create_service_dependency(
    service_id: str = Field(..., description="The ID of the service to add a dependency to"),
    dependent_service_id: str = Field(..., description="The ID of the dependent service"),
    relationship_type: str = Field(..., description="The type of relationship (e.g., 'uses', 'depends_on')")
) -> Dict[str, Any]:
    """Create a new service dependency.

    Args:
        service_id (str): The ID of the service to add a dependency to.
        dependent_service_id (str): The ID of the dependent service.
        relationship_type (str): The type of relationship (e.g., 'uses', 'depends_on').
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Created dependency data if successful"""
    try:
        with ApiClient(configuration) as api_client:
            service_dependencies_api = ServiceDependenciesApi(api_client)
            body = {
                "data": {
                    "type": "service_dependency",
                    "attributes": {
                        "dependent_service_id": dependent_service_id,
                        "relationship_type": relationship_type,
                    },
                }
            }
            response = service_dependencies_api.create_service_dependency(service_id, body=body)
            return {"status": "success", "message": "Service dependency created successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while creating service dependency: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while creating service dependency: {e}"}

@mcp.tool()
def delete_service_dependency(
    service_id: str = Field(..., description="The ID of the service to delete a dependency from"),
    dependency_id: str = Field(..., description="The ID of the dependency to delete")
) -> Dict[str, Any]:
    """Delete a specific service dependency.

    Args:
        service_id (str): The ID of the service to delete a dependency from.
        dependency_id (str): The ID of the dependency to delete.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            service_dependencies_api = ServiceDependenciesApi(api_client)
            service_dependencies_api.delete_service_dependency(service_id, dependency_id)
            return {"status": "success", "message": "Service dependency deleted successfully"}
    except ApiException as e:
        return {"status": "error", "message": f"API error while deleting service dependency: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while deleting service dependency: {e}"}
