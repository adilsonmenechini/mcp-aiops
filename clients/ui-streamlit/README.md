# MCP aiops UI Client (Streamlit)

This directory contains the Streamlit-based UI client for the MCP aiops project. This client provides a user-friendly interface to interact with the various MCP servers and their exposed tools.

## Features

- **Interactive Chat Interface**: Communicate with the MCP agent and receive responses.
- **Tool Execution Visualization**: See which tools the agent is using and their outputs.
- **Dynamic Tool Discovery**: Automatically discovers and displays tools from connected MCP servers.
- **Configurable LLM Providers**: Easily switch between different Large Language Models (LLMs) like OpenAI, Anthropic, Ollama, and Google Gemini.
- **Session Management**: Chat history and settings are maintained across sessions.

## Project Structure

```
.env-examples
.python-version
.streamlit/
├── config.toml
└── style.css
Dockerfile
README.md
app.py
apps/
├── __init__.py
└── mcp_aiops.py
config.py
icons/
└── aiops.png
pyproject.toml
requirements.txt
servers_config.json
services/
├── __init__.py
├── ai_service.py
├── chat_service.py
└── mcp_service.py
ui_components/
├── __init__.py
├── main_components.py
└── sidebar_components.py
utils/
├── __init__.py
├── ai_prompts.py
├── async_helpers.py
└── tool_schema_parser.py
uv.lock
```

## Installation

To set up the Streamlit UI client, follow these steps:

1.  **Navigate to the client directory**:

    ```bash
    cd clients/ui-streamlit
    ```

2.  **Install dependencies**:

    It is recommended to use `uv` for dependency management. If you don't have `uv` installed, you can install it via `pip`:

    ```bash
    pip install uv
    ```

    Then, install the project dependencies:

    ```bash
    uv sync
    ```

    Alternatively, you can use `pip`:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### Environment Variables

Create a `.env` file in the `clients/ui-streamlit/` directory based on the `.env-examples` file. This file will contain your API keys and other sensitive information.

Example `.env` file:

```dotenv
# Google Gemini API Key (for 'Google' LLM provider)
GEMINI_API_KEY="your_gemini_api_key_here"

# OpenAI API Key (for 'OpenAI' LLM provider, if enabled in config.py)
OPENAI_API_KEY="your_openai_api_key_here"

# Anthropic API Key (for 'Anthropic' LLM provider, if enabled in config.py)
ANTHROPIC_API_KEY="your_anthropic_api_key_here"

# Ollama Host (for 'Ollama' LLM provider, if enabled in config.py)
OLLAMA_HOST="http://localhost:11434"
```

### Server Configuration

The `servers_config.json` file defines the MCP servers that this UI client will connect to. An example `servers_config.json` is provided. Ensure it is correctly configured to point to your running MCP servers.

Example `servers_config.json`:

```json
{
  "mcpServers": {
    "datadog": {
      "url": "http://localhost:8000"
    },
    "duckduckgo": {
      "url": "http://localhost:8001"
    }
  }
}
```

## Usage

To run the Streamlit UI client, execute the following command from the `clients/ui-streamlit/` directory:

```bash
streamlit run app.py
```

This will open the Streamlit application in your web browser, usually at `http://localhost:8501`.

## Extending the UI Client

- **Adding new LLM providers**: Modify `config.py` and `services/ai_service.py` to integrate new LLMs.
- **Customizing UI components**: Explore `ui_components/` to adjust the layout and appearance.
- **Integrating new features**: Add new functionalities by extending `apps/mcp_aiops.py` and creating new services in `services/`.