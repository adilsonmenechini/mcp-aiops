from typing import Optional, Dict, Any, List
from pydantic import Field
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
from config import configuration
from mcp.server.fastmcp import FastMCP
from datadog_api_client.exceptions import (
    ApiException
)

mcp = FastMCP("Datadog Metrics Service")

@mcp.tool()
def query_metrics(
    query: str = Field(..., description="The query to execute"),
    from_time: int = Field(..., description="Start time in epoch seconds"),
    to_time: int = Field(..., description="End time in epoch seconds")
) -> Dict[str, Any]:
    """Query metrics from Datadog.

    Args:
        query (str): The query to execute.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Query results if successful"""
    try:
        with ApiClient(configuration) as api_client:
            metrics_api = MetricsApi(api_client)
            response = metrics_api.query_metrics(from_time, to_time, query)
            return {"status": "success", "message": "Metrics queried successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error querying metrics: {e}"}

@mcp.tool()
def list_metrics(
    q: Optional[str] = Field(default=None, description="Query to filter metrics")
) -> Dict[str, Any]:
    """List available metrics.

    Args:
        q (Optional[str], optional): Query to filter metrics.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): List of available metrics if successful"""
    try:
        with ApiClient(configuration) as api_client:
            metrics_api = MetricsApi(api_client)
            response = metrics_api.list_metrics(q=q)
            return {"status": "success", "message": "Metrics listed successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error listing metrics: {e}"}

@mcp.tool()
def update_metric_metadata(
    metric_name: str = Field(..., description="The name of the metric"),
    type: Optional[str] = Field(default=None, description="The type of the metric (e.g., 'gauge', 'count')"),
    description: Optional[str] = Field(default=None, description="A description of the metric"),
    unit: Optional[str] = Field(default=None, description="The unit of the metric")
) -> Dict[str, Any]:
    """Update metadata for a metric.

    Args:
        metric_name (str): The name of the metric.
        type (Optional[str], optional): The type of the metric (e.g., 'gauge', 'count').
        description (Optional[str], optional): A description of the metric.
        unit (Optional[str], optional): The unit of the metric.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Updated metadata if successful"""
    try:
        with ApiClient(configuration) as api_client:
            metrics_api = MetricsApi(api_client)
            body = {}
            if type:
                body["type"] = type
            if description:
                body["description"] = description
            if unit:
                body["unit"] = unit
            response = metrics_api.update_metric_metadata(metric_name, body=body)
            return {"status": "success", "message": "Metric metadata updated successfully", "content": response.to_dict()}
    except Exception as e:
        return {"status": "error", "message": f"Error updating metric metadata: {e}"}

@mcp.tool()
def delete_metric_metadata(
    metric_name: str = Field(..., description="The name of the metric to delete metadata for")
) -> Dict[str, Any]:
    """Delete metadata for a metric.

    Args:
        metric_name (str): The name of the metric to delete metadata for.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result"""
    try:
        with ApiClient(configuration) as api_client:
            metrics_api = MetricsApi(api_client)
            metrics_api.delete_metric_metadata(metric_name)
            return {"status": "success", "message": "Metric metadata deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error deleting metric metadata: {e}"}

@mcp.tool()
def query_p99_latency(
    service_name: str = Field(..., description="The name of the service to query"),
    from_time: int = Field(..., description="Start time in epoch seconds"),
    to_time: int = Field(..., description="End time in epoch seconds")
) -> Dict[str, Any]:
    """Query P99 latency for a specific service.

    Args:
        service_name (str): The name of the service to query.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): P99 latency metrics if successful"""
    try:
        with ApiClient(configuration) as api_client:
            metrics_api = MetricsApi(api_client)
            query = f"avg:trace.{service_name}.duration{99}percent"
            response = metrics_api.query_metrics(from_time, to_time, query)
            return {"status": "success", "message": "P99 latency retrieved successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while querying P99 latency: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while querying P99 latency: {e}"}

@mcp.tool()
def query_error_rate(
    service_name: str = Field(..., description="The name of the service to query"),
    from_time: int = Field(..., description="Start time in epoch seconds"),
    to_time: int = Field(..., description="End time in epoch seconds")
) -> Dict[str, Any]:
    """Query error rate for a specific service.

    Args:
        service_name (str): The name of the service to query.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Error rate metrics if successful"""
    try:
        with ApiClient(configuration) as api_client:
            metrics_api = MetricsApi(api_client)
            query = f"avg:trace.{service_name}.errors{99}percent"
            response = metrics_api.query_metrics(from_time, to_time, query)
            return {"status": "success", "message": "Error rate retrieved successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while querying error rate: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while querying error rate: {e}"}

@mcp.tool()
def query_downstream_latency(
    service_name: str = Field(..., description="The name of the downstream service to query"),
    from_time: int = Field(..., description="Start time in epoch seconds"),
    to_time: int = Field(..., description="End time in epoch seconds")
) -> Dict[str, Any]:
    """Query latency for a downstream service.

    Args:
        service_name (str): The name of the downstream service to query.
        from_time (int): Start time in epoch seconds.
        to_time (int): End time in epoch seconds.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - message (str): Description of the operation result
            - content (dict): Downstream latency metrics if successful"""
    try:
        with ApiClient(configuration) as api_client:
            metrics_api = MetricsApi(api_client)
            query = f"avg:trace.{service_name}.downstream.duration{99}percent"
            response = metrics_api.query_metrics(from_time, to_time, query)
            return {"status": "success", "message": "Downstream latency retrieved successfully", "content": response.to_dict()}
    except ApiException as e:
        return {"status": "error", "message": f"API error while querying downstream latency: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error while querying downstream latency: {e}"}
