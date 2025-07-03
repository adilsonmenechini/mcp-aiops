from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.downtimes_api import DowntimesApi
from config import configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datadog Downtime Service")

class DowntimeResponse(BaseModel):
    id: int
    scope: str
    message: str
    start: int
    end: int

@mcp.tool()
def create_downtime(
    scope: str = Field(..., description="The scope to apply the downtime to"),
    message: str = Field(default="", description="The message for the downtime"),
    start: int = Field(default_factory=lambda: int(time.time()), description="Start time in epoch seconds"),
    end: Optional[int] = Field(default=None, description="End time in epoch seconds"),
    timezone: str = Field(default="UTC", description="Timezone for the downtime")
) -> Dict[str, Any]:
    """Create a new downtime.
    
    Args:
        scope (str): The scope to apply the downtime to.
        message (str, optional): The message for the downtime.
        start (int, optional): Start time in epoch seconds. Defaults to current time.
        end (Optional[int], optional): End time in epoch seconds.
        timezone (str, optional): Timezone for the downtime. Defaults to "UTC".

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Response data from the API if successful"""
    try:
        with ApiClient(configuration) as api_client:
            downtimes_api = DowntimesApi(api_client)
            body = {
                "data": {
                    "type": "downtime",
                    "attributes": {
                        "scope": scope,
                        "message": message,
                        "start": start,
                        "end": end,
                        "timezone": timezone,
                    },
                }
            }
            response = downtimes_api.create_downtime(body)
            return {"status": "success", "message": "Downtime created successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error creating downtime: {e}"}

@mcp.tool()
def update_downtime(
    downtime_id: str = Field(..., description="The ID of the downtime to update"),
    scope: Optional[str] = Field(default=None, description="The new scope for the downtime"),
    message: Optional[str] = Field(default=None, description="The new message for the downtime"),
    end: Optional[int] = Field(default=None, description="The new end time in epoch seconds")
) -> Dict[str, Any]:
    """Update an existing downtime.

    Args:
        downtime_id (str): The ID of the downtime to update.
        scope (Optional[str], optional): The new scope for the downtime.
        message (Optional[str], optional): The new message for the downtime.
        end (Optional[int], optional): The new end time in epoch seconds.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Response data from the API if successful"""
    try:
        with ApiClient(configuration) as api_client:
            downtimes_api = DowntimesApi(api_client)
            body = {"data": {"type": "downtime", "id": downtime_id, "attributes": {}}}
            if scope:
                body["data"]["attributes"]["scope"] = scope
            if message:
                body["data"]["attributes"]["message"] = message
            if end:
                body["data"]["attributes"]["end"] = end
            response = downtimes_api.update_downtime(downtime_id, body)
            return {"status": "success", "message": "Downtime updated successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error updating downtime: {e}"}

@mcp.tool()
def cancel_downtime(
    downtime_id: str = Field(..., description="The ID of the downtime to cancel")
) -> Dict[str, Any]:
    """Cancel an existing downtime.

    Args:
        downtime_id (str): The ID of the downtime to cancel.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            downtimes_api = DowntimesApi(api_client)
            downtimes_api.cancel_downtime(downtime_id)
            return {"status": "success", "message": "Downtime canceled successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error canceling downtime: {e}"}
