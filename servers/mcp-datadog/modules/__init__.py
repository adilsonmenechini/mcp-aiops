# Import tools from all modules
from .monitor import (
    get_monitor_status,
    create_monitor_config_policy,
    update_monitor_config_policy,
    delete_monitor_config_policy,
    list_monitor_config_policies,
    search_monitors,
    create_monitor,
    delete_monitor,
    get_monitor,
    update_monitor,
)
from .dashboard import list_dashboards, list_prompts
from .downtime import create_downtime, update_downtime, cancel_downtime
from .host import list_hosts, mute_host, unmute_host, get_host_totals
from .incident import search_incidents, list_incidents, get_incident
from .trace import list_traces
from .metrics import query_metrics, list_metrics, query_p99_latency, query_error_rate, query_downstream_latency
from .logs import archive_logs
from .events import delete_event, search_events, get_event
from .tags import list_host_tags, add_host_tags, delete_host_tags
from .users import list_users, get_user
from .roles import list_roles, get_role, create_role, delete_role, update_role
from .service_checks import submit_service_check, list_service_checks
from .usage import get_hourly_usage
from .alerts import mute_alert, unmute_alert
from .apm import query_apm_errors, query_apm_latency, query_apm_spans
from .root_cause import analyze_service_with_apm
# List of tools for registration
mcp_tools = [
    ## Monitor tools
    #get_monitor_status,
    create_monitor_config_policy,
    update_monitor_config_policy,
    delete_monitor_config_policy,
    list_monitor_config_policies,
    search_monitors,
    create_monitor,
    delete_monitor,
    get_monitor,
    update_monitor,
    ## Dashboard tools
    list_dashboards,
    list_prompts,
    ## Downtime tools
    create_downtime,
    update_downtime,
    cancel_downtime,
    ## Host tools
    list_hosts,
    # mute_host,
    # unmute_host,
    get_host_totals,
    ## Incident tools
    search_incidents,
    list_incidents,
    get_incident,
    ## Trace tools
    list_traces,
    ## Metrics tools
    query_metrics,
    list_metrics,
    query_p99_latency,
    query_error_rate,
    query_downstream_latency,
    ## Logs tools
    # archive_logs,
    ## Events tools
    # delete_event,
    search_events,
    get_event,
    # Tags tools
    list_host_tags,
    # add_host_tags,
    # delete_host_tags,
    # Users tools
    # list_users,
    # get_user,
    # Roles tools
    # list_roles,
    # get_role,
    # create_role,
    # delete_role,
    # update_role,
    # Service Checks tools
    submit_service_check,
    list_service_checks,
    # Usage tools
    get_hourly_usage,
    # Alerts tools
    mute_alert,
    unmute_alert,
    # APM tools
    query_apm_errors,
    query_apm_latency,
    query_apm_spans,
    # # Root Cause Analysis tools
    # analyze_service_with_apm,
]

# Todas as ferramentas já estão incluídas na lista mcp_tools acima
