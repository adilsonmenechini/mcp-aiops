import asyncio
import json
import logging
import os
from config import Configuration, LogLevel, sre_system_prompt
from src.service.server import Server
from src.model.llm_client import LLMClient # Importe LLMClient da sua nova localização
from src.chat_session import ChatSession

async def main() -> None:
    """
    Main function to set up and start the chat session.
    Loads configuration and initializes servers and LLM client.
    """
    config = Configuration()
    config.load_env() # Load environment variables
    LogLevel.configure_logging(os.getenv("LOG_LEVEL")) # Configure logging

    # Load server configurations
    server_config_path = "servers_config.json"
    if not os.path.exists(server_config_path):
        logging.error(f"Configuration file not found: {server_config_path}")
        print(f"Error: Configuration file '{server_config_path}' not found. Please create it.")
        return

    try:
        server_config = config.load_config(server_config_path)
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing {server_config_path}: {e}")
        print(f"Error: Could not parse '{server_config_path}'. Please check its JSON format.")
        return
    except Exception as e:
        logging.error(f"Error loading configuration from {server_config_path}: {e}")
        print(f"Error loading configuration: {e}")
        return

    servers = [Server(name, srv_config) for name, srv_config in server_config["mcpServers"].items()]

    llm_client = LLMClient() # Model name can be passed here if desired, e.g.
    chat_session = ChatSession(servers, llm_client, sre_system_prompt, llm_config_params=config.llm_config_params)
    await chat_session.start()


if __name__ == "__main__":
    asyncio.run(main())