from typing import Optional, Dict, Any
from pydantic import Field
from datadog_api_client import ApiClient
from datadog_api_client.v2.api.spans_api import SpansApi
from config import configuration
from mcp.server.fastmcp import FastMCP
from datadog_api_client.exceptions import (
    ApiException
)

mcp = FastMCP("Datadog APM Service")

@mcp.tool()
def list_apm_traces(
    query: str = Field(..., description="The query to filter traces"),
    from_time: int = Field(..., description="Start time in epoch seconds"),
    to_time: int = Field(..., description="End time in epoch seconds"),
    limit: int = Field(default=100, description="Maximum number of traces to return"),
    sort: str = Field(default="-timestamp", description="Sort order for traces (e.g., '-timestamp')")
) -> Dict[str, Any]:
    """List APM traces based on a query.
    
    Args:
        query (str): The query to filter traces.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
        limit (int): Maximum number of traces to return.
        sort (str): Sort order for traces (e.g., '-timestamp').
    
    Returns:
        Dict[str, Any]: A dictionary containing the status and message of the operation, along with the retrieved traces.
    """
    try:
        with ApiClient(configuration) as api_client:
            spans_api = SpansApi(api_client)
            response = spans_api.list_spans(
                body={
                    "data": {
                        "attributes": {
                            "filter": {
                                "query": query,
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
            return {"status": "success", "message": "APM traces retrieved successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while retrieving APM traces: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while retrieving APM traces: {e}"}

@mcp.tool()
def get_apm_trace_details(
    trace_id: str = Field(..., description="The unique ID of the trace to retrieve")
) -> Dict[str, Any]:
    """Retrieve details of a specific APM trace by ID.
    
    Args:
        trace_id (str): The unique ID of the trace to retrieve. 

    Returns:
        Dict[str, Any]: A dictionary containing the status and message of the operation, along with the trace details."""
    try:
        with ApiClient(configuration) as api_client:
            spans_api = SpansApi(api_client)
            response = spans_api.get_span(trace_id)
            return {"status": "success", "message": "APM trace details retrieved successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while retrieving APM trace details: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while retrieving APM trace details: {e}"}

@mcp.tool()
def summarize_apm_traces(
    query: str = Field(..., description="The query to filter traces"),
    from_time: int = Field(..., description="Start time in epoch seconds"),
    to_time: int = Field(..., description="End time in epoch seconds")
) -> Dict[str, Any]:
    """Summarize APM trace statistics.
    
    Args:
        query (str): The query to filter traces.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
    
    Returns:
        Dict[str, Any]: A dictionary containing the status and message of the operation, along with trace statistics
    """
    try:
        with ApiClient(configuration) as api_client:
            spans_api = SpansApi(api_client)
            response = spans_api.list_spans(
                body={
                    "data": {
                        "attributes": {
                            "filter": {
                                "query": query,
                                "from": str(from_time),
                                "to": str(to_time),
                            },
                            "page": {"limit": 1000},
                        },
                        "type": "search_request",
                    }
                }
            )
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
        return {"status": "error", "message": f"Error summarizing traces: {e}"}

@mcp.tool()
def query_apm_errors(
    service_name: str = Field(..., description="The name of the service to query errors for"),
    from_time: int = Field(..., description="Start time in epoch seconds"),
    to_time: int = Field(..., description="End time in epoch seconds")
) -> Dict[str, Any]:
    """Query error metrics for a specific APM service.
    
    Args:
        service_name (str): The name of the service to query errors for.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
    Returns:
        Dict[str, Any]: A dictionary containing the status and message of the operation, along with the error metrics.
    """
    try:
        with ApiClient(configuration) as api_client:
            spans_api = SpansApi(api_client)
            query = f"avg:trace.{service_name}.errors{99}percent"
            response = spans_api.list_spans(
                body={
                    "data": {
                        "attributes": {
                            "filter": {
                                "query": query,
                                "from": str(from_time),
                                "to": str(to_time),
                            },
                            "page": {"limit": 1000},
                        },
                        "type": "search_request",
                    }
                }
            )
            return {"status": "success", "message": "APM errors retrieved successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while querying APM errors: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while querying APM errors: {e}"}

@mcp.tool()
def query_apm_latency(
    service_name: str = Field(..., description="The name of the service to query latency for"),
    from_time: int = Field(..., description="Start time in epoch seconds"),
    to_time: int = Field(..., description="End time in epoch seconds")
) -> Dict[str, Any]:
    """Query latency metrics for a specific APM service.

    Args:
        service_name (str): The name of the service to query latency for.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
    
    Returns:
        Dict[str, Any]: A dictionary containing the status and message of the operation, along with the latency metrics."""
    try:
        with ApiClient(configuration) as api_client:
            spans_api = SpansApi(api_client)
            query = f"avg:trace.servlet.request.hits{{service:{service_name}}}"
            response = spans_api.list_spans(
                body={
                    "data": {
                        "attributes": {
                            "filter": {
                                "query": query,
                                "from": str(from_time),
                                "to": str(to_time),
                            },
                            "page": {"limit": 1000},
                        },
                        "type": "search_request",
                    }
                }
            )
            return {"status": "success", "message": "APM latency retrieved successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while querying APM latency: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while querying APM latency: {e}"}

@mcp.tool()
def query_apm_spans(
    service_name: str = Field(..., description="The name of the service to query spans for"),
    from_time: int = Field(..., description="Start time in epoch seconds"),
    to_time: int = Field(..., description="End time in epoch seconds")
) -> Dict[str, Any]:
    """Query spans for a specific APM service.

    Args:
        service_name (str): The name of the service to query spans for.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
    
    Returns:
        Dict[str, Any]: A dictionary containing the status and message of the operation, along with the retrieved spans."""
    try:
        with ApiClient(configuration) as api_client:
            spans_api = SpansApi(api_client)
            query = f"service:{service_name}"
            response = spans_api.list_spans(
                body={
                    "data": {
                        "attributes": {
                            "filter": {
                                "query": query,
                                "from": str(from_time),
                                "to": str(to_time),
                            },
                            "page": {"limit": 1000},
                        },
                        "type": "search_request",
                    }
                }
            )
            return {"status": "success", "message": "APM spans retrieved successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while querying APM spans: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while querying APM spans: {e}"}
