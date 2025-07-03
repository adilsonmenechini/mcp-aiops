from pydantic import BaseModel, Field
import json
import time
import logging
import sys
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from config import configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datadog Dashboards Service")

class DashboardResponse(BaseModel):
    id: str
    title: str
    url: str

dashboard_list_schema = {
    "type": "object",
    "properties": {
        "dashboards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "url": {"type": "string"}
                }
            }
        },
        "total": {"type": "integer"},
        "message": {"type": "string"}
    }
}

@mcp.tool()
def list_dashboards(
    name: str = Field(default=None, description="Filter dashboards by name"),
    tags: list[str] = Field(default=None, description="Filter dashboards by tags")
) -> dict:
    """Retrieves a list of Datadog dashboards with optional filtering by name and tags.

    Args:
        name (str, optional): Filter dashboards by name.
        tags (list[str], optional): Filter dashboards by tags.

    Returns:
        dict: A dictionary containing:
            - content (dict): Contains dashboards list, total count and status message
                - dashboards (list): List of dashboard objects with id, title and url
                - total (int): Total number of dashboards found
                - message (str): Status message of the operation"""
    try:
        with ApiClient(configuration) as api_client:
            dashboards_api = DashboardsApi(api_client)
            response = dashboards_api.list_dashboards(filter_shared=False)

            if response is not None and response.dashboards is not None:
                # Apply filters if provided
                filtered_dashboards = response.dashboards
                if name:
                    search_term = name.lower()
                    filtered_dashboards = [
                        d for d in filtered_dashboards if d.title and search_term in d.title.lower()
                    ]
                if tags:
                    filtered_dashboards = [
                        d for d in filtered_dashboards if set(tags).issubset(set(d.tags or []))
                    ]

                dashboards_data = [
                    DashboardResponse(
                        id=d.id,
                        title=d.title,
                        url=f"https://app.datadoghq.com/dashboard/{d.id}"
                    ).dict()
                    for d in filtered_dashboards
                ]

                result = {
                    "content": {
                        "dashboards": dashboards_data,
                        "total": len(dashboards_data),
                        "message": "Successfully retrieved dashboards."
                    }
                }
                return result
            else:
                result = {
                    "content": {
                        "dashboards": [],
                        "total": 0,
                        "message": "Error: Invalid response from Datadog API."
                    }
                }
                return result
    except Exception as e:
        return {
            "content": {
                "dashboards": [],
                "total": 0,
                "message": f"Error fetching dashboards: {e}"
            }
        }
    finally:
        pass

@mcp.tool()
def list_prompts() -> dict:
    """Placeholder function for prompts/list to avoid method not found errors.

    Args:
        None

    Returns:
        dict: A dictionary containing:
            - content (dict): Contains prompts information
                - prompts (list): Empty list of prompts
                - total (int): Total count of prompts (always 0)
                - message (str): Status message"""
    try:
        result = {
            "content": {
                "prompts": [],
                "total": 0,
                "message": "No prompts available."
            }
        }
        return result
    except Exception as e:
        return {
            "content": {
                "prompts": [],
                "total": 0,
                "message": f"Error fetching prompts: {e}"
            }
        }
    finally:
        pass
