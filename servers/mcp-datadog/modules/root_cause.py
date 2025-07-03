from typing import Dict, Any, Optional
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from .apm import query_apm_errors, query_apm_latency, query_apm_spans
from datadog_api_client.exceptions import (
    ApiException
)
import json
import time


mcp = FastMCP("Datadog Root Cause Analysis Service")

@mcp.tool()
def analyze_service_with_apm(
    service_name: str = Field(..., description="The name of the service to analyze"),
    from_time: Optional[int] = Field(None, description="Start time in epoch seconds. Defaults to 2 hours ago if not provided"), 
    to_time: Optional[int] = Field(None, description="End time in epoch seconds. Defaults to current time if not provided")
) -> Dict[str, Any]:
    """Perform root cause analysis for a service, including APM spans, errors, and latency.

    Args:
        service_name (str): The name of the service to analyze.
        from_time (Optional[int], optional): Start time in epoch seconds. Defaults to 2 hours ago if not provided.
        to_time (Optional[int], optional): End time in epoch seconds. Defaults to current time if not provided.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): 'success' or 'error'
            - service_name (str): Name of the analyzed service
            - time_range (dict): Time range of the analysis
                - from (int): Start time in epoch seconds
                - to (int): End time in epoch seconds
            - data (dict): Analysis results
                - latency (dict): Latency metrics data
                - errors (dict): Error metrics data
                - spans (dict): APM spans data
            - message (str): Error message if status is 'error'"""
    try:
        # Set default time range to last 2 hours if not provided
        current_time = int(time.time())
        to_time = to_time or current_time
        from_time = from_time or (current_time - 7200)  # 7200 seconds = 2 hours

        # Step 1: Query APM latency
        latency_result = query_apm_latency(service_name, from_time, to_time)
        if latency_result.get("status") != "success" or "data" not in latency_result:
            return {"status": "error", "message": "Failed to retrieve APM latency", "details": latency_result}

        # Step 2: Query APM errors
        error_result = query_apm_errors(service_name, from_time, to_time)
        if error_result.get("status") != "success" or "data" not in error_result:
            return {"status": "error", "message": "Failed to retrieve APM errors", "details": error_result}

        # Step 3: Query APM spans
        spans_result = query_apm_spans(service_name, from_time, to_time)
        if spans_result.get("status") != "success" or "data" not in spans_result:
            return {"status": "error", "message": "Failed to retrieve APM spans", "details": spans_result}

        # Structure the analysis result
        analysis_result = {
            "status": "success",
            "service_name": service_name,
            "time_range": {
                "from": from_time,
                "to": to_time
            },
            "data": {
                "latency": latency_result.get("data", {}),
                "errors": error_result.get("data", {}),
                "spans": spans_result.get("data", {})
            }
        }
        
        return analysis_result

    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error during root cause analysis with APM: {str(e)}"
        }
