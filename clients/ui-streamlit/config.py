import os
import json
from dotenv import load_dotenv

load_dotenv()
env = os.getenv

# Model mapping
MODEL_OPTIONS = {
    # 'OpenAI': 'gpt-4o',
    # 'Antropic': 'claude-3-5-sonnet-20240620',
    'Google': 'gemini-2.0-flash',
    'Ollama': 'mistral:instruct'
    }

# Streamlit defaults
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7

# Load server configuration
config_path = os.path.join('.', 'servers_config.json')
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        SERVER_CONFIG = json.load(f)