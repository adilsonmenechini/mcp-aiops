# SRE Chatbot with Multiple LLMs and MCP Tools

This project implements a command-line chatbot specialized in SRE (Site Reliability Engineering) that integrates with different Large Language Models (LLMs) and utilizes MCP (Model Context Protocol) servers to execute tools. The goal is to provide an intelligent assistant capable of aiding in reliability, performance, and incident response tasks, automating operations through tools.

## Description

The chatbot acts as a conversational interface where users can interact with an LLM. The LLM, in turn, is instructed to act as an SRE expert and has the ability to invoke external tools hosted on MCP servers. This modular architecture allows for easy extensibility, both in adding new LLMs and integrating new tools.

## Features

- **Multiple LLM Support**: Switches between Google Gemini, Ollama (local models), and Anthropic Claude through a simple environment variable configuration

- **LangChain Integration**: Utilizes the LangChain library for a unified and simplified interface with different LLM providers

- **MCP Tool Execution**: Capable of identifying and invoking tools available on configured MCP servers

- **Specialized SRE System Prompt**: The LLM is guided by a detailed system prompt to act as an SRE assistant, focusing on reliability and automation

- **Chat History Management**: Maintains conversation context for more coherent responses

- **Flexible Configuration**: LLM parameters (temperature, max tokens, etc.) and credentials are managed via environment variables

- **Retry Logic**: Includes a retry mechanism for LLM calls, increasing robustness

- **Detailed Logging**: Provides informative logs for debugging and monitoring

## Project Structure

```
.
├── main.py                     # Main application entry point
├── config.py                   # Classes for loading environment variables and configurations
├── servers_config.json         # Configurations for MCP servers
└── src/
    ├── __init__.py
    ├── chat_session.py         # Main chat logic and orchestration
    ├── model/
    │   ├── __init__.py
    │   ├── llm_client.py       # LLMClient factory and retry logic
    │   └── llm_clients/
    │       ├── __init__.py
    │       ├── base_llm_client.py  # Abstract base class for LLM clients
    │       ├── gemini_client.py    # LLM client for Google Gemini (via LangChain)
    │       ├── ollama_client.py    # LLM client for Ollama (via LangChain)
    │       └── anthropic_client.py # LLM client for Anthropic (via LangChain)
    └── service/
        ├── __init__.py
        └── server.py           # Manages connection and interaction with an MCP server
```

## Environment Setup

### Prerequisites

- Python 3.12+
- uv (optional, for efficient execution) or pip
- For Ollama: An instance of Ollama running locally and the desired models (e.g., `ollama pull llama3.2`)

### Installing Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt # If you have one, otherwise, install manually:
```

Install the necessary libraries:

```bash
pip install ollama anthropic langchain langchain-openai langchain-anthropic langchain-google-genai langchain-ollama python-dotenv
```

### Environment Variable Configuration (.env)

Create a `.env` file in the project root and configure the necessary environment variables. Choose an `LLM_PROVIDER` and provide the corresponding keys/models.

#### Example for Google Gemini:

```env
LLM_PROVIDER="gemini"
GOOGLE_API_KEY="YOUR_GEMINI_KEY_HERE"
GOOGLE_MODEL="gemini-1.5-flash" # Or another preferred model
```

#### Example for Ollama:

```env
LLM_PROVIDER="ollama"
OLLAMA_MODEL="mixtral" # Ensure this model is available in your Ollama instance
OLLAMA_API_BASE_URL="http://localhost:11434" # Change if your Ollama server is elsewhere
```

#### Example for Anthropic:

```env
LLM_PROVIDER="anthropic"
ANTHROPIC_API_KEY="YOUR_ANTHROPIC_KEY_HERE"
ANTHROPIC_MODEL="claude-3-haiku-20240307" # Or another Claude model
```

### servers_config.json

This file defines the MCP servers and the tools the chatbot can use. A basic example might be:

```json
{
  "mcpServers": {
    "local_server": {
      "command": "python",
      "args": ["path/to/your/mcp_server_script.py"],
      "env": {}
    }
  }
}
```

**Note**: You will need a real MCP server at `path/to/your/mcp_server_script.py` that exposes tools.

## How to Run

After configuring the environment and variables, run `main.py`:

```bash
uv run python main.py
# Or, if not using uv:
python main.py
```

## Usage

The chatbot will start, and you can interact with it via the command line.
Type your questions, and the SRE assistant will respond, triggering MCP tools when necessary.

To exit the chat, type `quit` or `exit`.

## Extensibility

### Add New LLMs

Create a new class in `src/model/llm_clients/` that inherits from `BaseLLMClient` and uses the corresponding LangChain wrapper. Then, add it to the `LLMClient` factory logic.

### Add New Tools

Develop new MCP servers that expose tools and add them to `servers_config.json`. The chatbot will automatically discover and use these tools.

## Contribution

Contributions are welcome! Feel free to open issues or pull requests in the repository.

## License

[Specify your project's license here, e.g., MIT, Apache 2.0, etc.]

