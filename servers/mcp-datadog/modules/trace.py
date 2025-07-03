from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import json
import time
from datadog_api_client import ApiClient
from datadog_api_client.v2.api.spans_api import SpansApi
from config import configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datadog Traces Service")

@mcp.tool()
def list_traces(
    query: str,
    from_time: int = Field(default_factory=lambda: int(time.time()) - 900, description="Start time in epoch seconds (default: last 15 minutes)"),
    to_time: int = Field(default_factory=lambda: int(time.time()), description="End time in epoch seconds (default: now)"),
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of traces to return (default: 100)"),
    sort: str = Field(default="-timestamp", description="Sort order for traces, default is descending timestamp"),
    service: Optional[str] = Field(default=None, description="Filter by service name"),
    operation: Optional[str] = Field(default=None, description="Filter by operation name")
) -> Dict[str, Any]:
    """Retrieves APM traces from Datadog.

    Args:
        query (str): Query to filter traces.
        from_time (int, optional): Start time in epoch seconds. Defaults to last 15 minutes.
        to_time (int, optional): End time in epoch seconds. Defaults to current time.
        limit (int, optional): Maximum number of traces to return (1-1000). Defaults to 100.
        sort (str, optional): Sort order for traces. Defaults to "-timestamp".
        service (Optional[str], optional): Filter by service name.
        operation (Optional[str], optional): Filter by operation name.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (List): List of trace data as formatted JSON text"""
    try:
        with ApiClient(configuration) as api_client:
            spans_api = SpansApi(api_client)
            filter_query = [query]
            if service:
                filter_query.append(f"service:{service}")
            if operation:
                filter_query.append(f"operation:{operation}")

            response = spans_api.list_spans(
                body={
                    "data": {
                        "attributes": {
                            "filter": {
                                "query": " ".join(filter_query),
                                "from": str(from_time),
                                "to": str(to_time),
                            },
                            "sort": sort,
                            "page": {"limit": limit},
                        },
                        "type": "search_request",
                    }
                }
            )

            if not response.data:
                return {"status": "error", "message": "No traces data returned", "content": []}

            return {
                "status": "success",
                "message": "Traces retrieved successfully",
                "content": [{"type": "text", "text": json.dumps(response.data, indent=2)}]
            }
    except Exception as e:
        return {"status": "error", "message": f"Error fetching traces: {e}", "content": []}

@mcp.tool()
def get_trace_details(
    trace_id: str = Field(..., description="The unique ID of the trace to retrieve")
) -> Dict[str, Any]:
    """Retrieve details of a specific trace by ID.

    Args:
        trace_id (str): The unique ID of the trace to retrieve.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (List): List containing trace details as formatted JSON text"""
    try:
        with ApiClient(configuration) as api_client:
            spans_api = SpansApi(api_client)
            response = spans_api.get_span(trace_id)

            if not response.data:
                return {"status": "error", "message": "No trace data returned", "content": []}

            return {
                "status": "success",
                "message": "Trace details retrieved successfully",
                "content": [{"type": "text", "text": json.dumps(response.data, indent=2)}]
            }
    except Exception as e:
        return {"status": "error", "message": f"Error fetching trace details: {e}", "content": []}

@mcp.tool()
def summarize_traces(
    query: str = Field(..., description="Query to filter traces"),
    from_time: int = Field(default_factory=lambda: int(time.time()) - 900, description="Start time in epoch seconds"),
    to_time: int = Field(default_factory=lambda: int(time.time()), description="End time in epoch seconds")
) -> Dict[str, Any]:
    """Summarize trace statistics for a given query.

    Args:
        query (str): Query to filter traces.
        from_time (int, optional): Start time in epoch seconds. Defaults to last 15 minutes.
        to_time (int, optional): End time in epoch seconds. Defaults to current time.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Summary statistics including:
                - trace_count (int): Number of traces found
                - services (list): List of unique service names"""
    try:
        with ApiClient(configuration) as api_client:
            spans_api = SpansApi(api_client)
            filter_query = [query]

            response = spans_api.list_spans(
                body={
                    "data": {
                        "attributes": {
                            "filter": {
                                "query": " ".join(filter_query),
                                "from": from_time,
                                "to": to_time,
                            },
                            "page": {"limit": 1000},
                        },
                        "type": "search_request",
                    }
                }
            )

            if not response.data:
                return {"status": "error", "message": "No trace data returned", "content": []}

            trace_count = len(response.data)
            services = set(d.attributes.get("service", "unknown") for d in response.data)

            return {
                "status": "success",
                "message": "Trace summary retrieved successfully",
                "content": {
                    "trace_count": trace_count,
                    "services": list(services)
                }
            }
    except Exception as e:
        return {"status": "error", "message": f"Error summarizing traces: {e}", "content": []}
