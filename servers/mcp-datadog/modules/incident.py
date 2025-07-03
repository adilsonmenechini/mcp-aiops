from pydantic import BaseModel, Field
import json
import logging
import sys
from datadog_api_client import ApiClient
from datadog_api_client.v2.api.incidents_api import IncidentsApi
from config import configuration
from mcp.server.fastmcp import FastMCP
from typing import Optional

mcp = FastMCP("Datadog Incident Service")


configuration.unstable_operations["search_incidents"] = True
configuration.unstable_operations["list_incidents"] = True
configuration.unstable_operations["get_incident"] = True
configuration.unstable_operations["update_incident"] = True
configuration.unstable_operations["delete_incident"] = True

@mcp.tool()
def search_incidents(
    query: str = Field(..., description="The search query to filter incidents"),
    page_size: int = Field(10, ge=1, le=100, description="Number of incidents per page (1-100, default: 10)"),
    page_offset: int = Field(0, ge=0, description="Page offset for pagination (>= 0, default: 0)"),
    ) -> dict:
    """Searches for incidents in Datadog based on a query.

    Args:
        query (str): The search query to filter incidents.
        page_size (int): Number of incidents per page (1-100, default: 10).
        page_offset (int): Page offset for pagination (>= 0, default: 0).

    Returns:
        dict: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (list): List of incidents data as JSON strings"""
    with ApiClient(configuration) as api_client:
        api_instance = IncidentsApi(api_client)
        try:
            response = api_instance.search_incidents(
                query=query,
                page_size=page_size,
                page_offset=page_offset
            )
                        
            return {
                "status": "success",
                "message": "Incidents retrieved successfully",
                "content": response.to_dict()
            }
        except Exception as e:
            return {"error": f"Failed to search incidents: {e}"}

@mcp.tool()
def list_incidents(
    page_size: int = Field(10, ge=1, le=100, description="Number of incidents per page (1-100, default: 10)"),
    page_offset: int = Field(0, ge=0, description="Page offset for pagination (>= 0, default: 0)"),
) -> dict:
    """Retrieves a list of incidents from Datadog.
    
    Args:
        page_size (int): Number of incidents per page (1-100, default: 10).
        page_offset (int): Page offset for pagination (>= 0, default: 0).
    
    Returns:
        dict: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (list): List of incidents data as JSON strings"""
    try:
        with ApiClient(configuration) as api_client:
            incidents_api = IncidentsApi(api_client)
            response = incidents_api.list_incidents(
                page_size=page_size, 
                page_offset=page_offset
            )

            if not response.data:
                return {"status": "error", "message": "No incidents data returned", "content": []}

            return {
                "status": "success",
                "message": "Incidents retrieved successfully",
                "content": response.to_dict()
            }
    except Exception as e:
        return {"status": "error", "message": f"Error fetching incidents: {e}", "content": []}
    finally:
        pass

@mcp.tool()
def get_incident(
    incident_id: str = Field(..., description="The ID of the incident to retrieve"),
    ) -> dict:
    """Retrieves a specific incident from Datadog.
    
    Args:
        incident_id (str): The ID of the incident to retrieve
    
    Returns:
        dict: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (list): List with a single text element containing incident data as JSON string
                - type (str): Type of content ('text')
                - text (str): JSON string with incident data"""
    try:
        with ApiClient(configuration) as api_client:
            incidents_api = IncidentsApi(api_client)
            response = incidents_api.get_incident(incident_id)

            if not response.data:
                return {"status": "error", "message": "No incident data returned", "content": []}

            return {
                "status": "success",
                "message": "Incidents retrieved successfully",
                "content": response.to_dict()
            }
    except Exception as e:
        return {"status": "error", "message": f"Error fetching incident: {e}", "content": []}
    finally:
        pass

@mcp.tool()
def update_incident(
    incident_id: str = Field(..., description="The ID of the incident to update"),
    title: Optional[str] = None , 
    status: Optional[str] = None,
    ) -> dict:
    """Update an existing incident.
    
    Args:
        incident_id (str): The ID of the incident to update.
        title (Optional[str], optional): New title for the incident.
        status (Optional[str], optional): New status for the incident.
    
    Returns:
        dict: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Updated incident data or empty list on error"""
    try:
        with ApiClient(configuration) as api_client:
            incidents_api = IncidentsApi(api_client)
            body = {"data": {"attributes": {}}}
            if title:
                body["data"]["attributes"]["title"] = title
            if status:
                body["data"]["attributes"]["status"] = status

            response = incidents_api.update_incident(incident_id, body=body)
            return {"status": "success", "message": "Incident updated successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error updating incident: {e}", "content": []}

@mcp.tool()
def delete_incident(
    incident_id: str = Field(..., description="The ID of the incident to delete"),
    ) -> dict:
    """Delete an incident.
    
    Args:
        incident_id (str): The ID of the incident to delete.
    
    Returns:
        dict: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            incidents_api = IncidentsApi(api_client)
            incidents_api.delete_incident(incident_id)
            return {"status": "success", "message": "Incident deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error deleting incident: {e}"}
