from typing import Optional, Dict, Any
from pydantic import Field
from datadog_api_client import ApiClient
from config import configuration
from mcp.server.fastmcp import FastMCP
from datadog_api_client.v1.api.events_api import EventsApi as EventsApiV1
from datadog_api_client.v2.api.events_api import EventsApi as EventsApiV2
from datadog_api_client.v2.model.events_list_request import EventsListRequest
from datadog_api_client.v2.model.events_query_filter import EventsQueryFilter
from datadog_api_client.v2.model.events_request_page import EventsRequestPage
from datadog_api_client.v2.model.events_sort import EventsSort

mcp = FastMCP("Datadog Events Service")



@mcp.tool()
def search_events(
    query = Field(..., description="The search query to filter events"),
    from_time = Field(..., description="Start time in epoch seconds"),
    to_time = Field(..., description="End time in epoch seconds"),
    limit: int = Field(default=5, description="Maximum number of events to return"),
    ) -> Dict[str, Any]:

    """
    Searches for events in Datadog based on a query and time range.
    
    Args:
        query (str): The search query to filter events.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
        limit (int): Maximum number of events to return. Default is 5.
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (list): List of events if successful
    """
    try:
        # Criar o corpo da requisição
        body = EventsListRequest(
            filter=EventsQueryFilter(
                query=query,
                _from=str(from_time),  # Garante que o timestamp seja string
                to=str(to_time)        # Garante que o timestamp seja string
            ),
            sort=EventsSort.TIMESTAMP_ASCENDING,
            page=EventsRequestPage(
                limit=limit
            )
        )

        # Fazer a chamada à API
        with ApiClient(configuration) as api_client:
            api_instance = EventsApiV2(api_client)
            response = api_instance.search_events(body=body)
            return {
                "status": "success",
                "message": "Incidents retrieved successfully",
                "content": response.to_dict()
            }
            
    except Exception as e:
        return {"error": str(e), "details": "Failed to search events"}

@mcp.tool()
def get_event(
    event_id: int = Field(..., description="The ID of the event to retrieve")
    ) -> Dict[str, Any]:
    """
    Retrieves details for a specific event by its ID.

    Args:
        event_id (int): The ID of the event to retrieve.
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): The event details if successful
    """
    try:
        with ApiClient(configuration) as api_client:
            api_instance = EventsApiV1(api_client)
            response = api_instance.get_event(
                event_id=int(event_id),
                )
            return {
                "status": "success",
                "message": "Incidents retrieved successfully",
                "content": response.to_dict()
            }
    except Exception as e:
        return {"error": str(e), "details": "Failed to get event"}
        
@mcp.tool()
def delete_event(
    event_id: int = Field(..., description="The ID of the event to delete")
) -> Dict[str, Any]:
    """Delete a specific event.

    Args:
        event_id (int): The ID of the event to delete.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            events_api = EventsApiV1(api_client)
            events_api.delete_event(event_id)
            return {"status": "success", "message": "Event deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error deleting event: {e}"}
