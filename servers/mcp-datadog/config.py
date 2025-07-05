import os
from dotenv import load_dotenv
from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v2.api.users_api import UsersApi
from datadog_api_client.v2.model.user import User

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

def check_datadog_auth():
    if not DATADOG_API_KEY or not DATADOG_APP_KEY:
        print("❌ ERROR: DATADOG_API_KEY or DATADOG_APP_KEY not found in environment variables.")
        return False

    try:
        with ApiClient(configuration) as api_client:
            api_instance = UsersApi(api_client)
            # Try to get the current user or a list of users
            # This call requires valid API and Application keys
            current_user_response = api_instance.get_current_user()
            
            if isinstance(current_user_response.data, User):
                print(f"✅ Authentication successful! Logged in as: {current_user_response.data.attributes.handle}")
                return True
            else:
                print("⚠️ Authentication might be partially successful, but could not retrieve user data.")
                return False

    except Exception as e:
        print(f"❌ Authentication failed! Error: {e}")
        print("Please check your DATADOG_API_KEY, DATADOG_APP_KEY, and DATADOG_SITE settings.")
        return False

if __name__ == "__main__":
    print("Attempting to verify Datadog API authentication...")
    if check_datadog_auth():
        print("Datadog API authentication is configured correctly.")
    else:
        print("Datadog API authentication failed. Please review your setup.")