import os
from dotenv import load_dotenv
from datadog_api_client import Configuration

# Load environment variables
load_dotenv()

# Datadog API Credentials
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY")
DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")

# Initialize Datadog API Configuration
configuration = Configuration()
configuration.api_key["apiKeyAuth"] = DATADOG_API_KEY
configuration.api_key["appKeyAuth"] = DATADOG_APP_KEY
configuration.server_variables["site"] = DATADOG_SITE
configuration.verify_ssl = True  # Consider setting to True for production
# configuration.debug = True  # Enable debug mode
