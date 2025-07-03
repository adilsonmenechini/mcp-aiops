import asyncio
import logging
import os
import shutil
from contextlib import AsyncExitStack
from typing import Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class Server:
    """
    Manages the connection to a single Model Context Protocol (MCP) server.
    Handles server initialization, listing available tools, executing tools,
    and proper cleanup of resources.
    """
    def __init__(self, name: str, config: dict[str, Any]) -> None:
        self.name: str = name
        self.config: dict[str, Any] = config
        self.stdio_context: Any | None = None
        self.session: ClientSession | None = None
        self._cleanup_lock: asyncio.Lock = asyncio.Lock()
        self.exit_stack: AsyncExitStack = AsyncExitStack()

    async def initialize(self) -> None:
        """
        Initializes the connection to the MCP server.
        Sets up the stdio client and the MCP client session.
        """
        command = shutil.which("npx") if self.config["command"] == "npx" else self.config["command"]
        if command is None:
            raise ValueError("The command must be a valid string and cannot be None.")

        server_params = StdioServerParameters(
            command=command,
            args=self.config["args"],
            env={**os.environ, **self.config["env"]} if self.config.get("env") else None,
        )
        try:
            logging.info(f"Initializing server {self.name} with command: {command} {self.config['args']}")
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self.session = session
            logging.info(f"Server {self.name} initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing server {self.name}: {e}")
            await self.cleanup()
            raise

    async def list_tools(self) -> list[Any]:
        """
        Lists the tools available on the connected MCP server.
        """
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        logging.info(f"Listing tools for server {self.name}...")
        tools_response = await self.session.list_tools()
        tools = []

        for item in tools_response:
            if isinstance(item, tuple) and item[0] == "tools":
                tools.extend(
                    Tool(tool.name, tool.description, tool.inputSchema, getattr(tool, 'title', None))
                    for tool in item[1]
                )
        logging.info(f"Found {len(tools)} tools on server {self.name}.")
        return tools

    async def execute_tool(self, tool_name: str, arguments: dict[str, Any], retries: int = 2, delay: float = 1.0) -> Any:
        """
        Executes a specific tool on the MCP server with provided arguments.
        Includes a retry mechanism for transient errors.
        """
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        attempt = 0
        while attempt < retries:
            try:
                logging.info(f"Attempting to execute tool '{tool_name}' on server {self.name} (Attempt {attempt + 1}/{retries})")
                logging.debug(f"Arguments for '{tool_name}': {arguments}") # Log arguments for debugging

                result = await self.session.call_tool(tool_name, arguments)
                logging.debug(f"Raw result from tool '{tool_name}': {result}") # Log raw result

                if isinstance(result, dict) and "progress" in result and "total" in result:
                    progress = result["progress"]
                    total = result["total"]
                    if total > 0:
                        percentage = (progress / total) * 100
                        logging.info(f"Tool '{tool_name}' progress: {progress}/{total} ({percentage:.1f}%)")
                    else:
                        logging.info(f"Tool '{tool_name}' progress: {progress}/{total} (Total is zero)")
                logging.info(f"Tool '{tool_name}' executed successfully.")
                return result
            except Exception as e:
                attempt += 1
                logging.error(f"Error executing tool '{tool_name}' on server {self.name}: {e}. Attempt {attempt} of {retries}.")
                if attempt < retries:
                    logging.info(f"Retrying tool '{tool_name}' in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logging.critical(f"Max retries reached for tool '{tool_name}'. Failing after {retries} attempts.")
                    raise # Re-raise the exception after max retries

    async def cleanup(self) -> None:
        """
        Cleans up the resources associated with the MCP server session.
        """
        async with self._cleanup_lock:
            if self.session:
                logging.info(f"Cleaning up server {self.name}...")
            try:
                await self.exit_stack.aclose()
                self.session = None
                self.stdio_context = None
                logging.info(f"Server {self.name} cleaned up.")
            except Exception as e:
                logging.error(f"Error during cleanup of server {self.name}: {e}")


class Tool:
    """
    Represents a tool available through an MCP server.
    Provides a method to format its description for LLM consumption.
    """
    def __init__(self, name: str, description: str, input_schema: dict[str, Any], title: str | None = None) -> None:
        self.name: str = name
        self.title: str | None = title
        self.description: str = description
        self.input_schema: dict[str, Any] = input_schema

    def format_for_llm(self) -> str:
        """
        Formats the tool's information into a human-readable string suitable for an LLM.
        """
        args_desc = []
        if "properties" in self.input_schema:
            for param_name, param_info in self.input_schema["properties"].items():
                arg_desc = f"- {param_name}: {param_info.get('description', 'No description')}"
                if param_name in self.input_schema.get("required", []):
                    arg_desc += " (required)"
                args_desc.append(arg_desc)

        output = f"Tool: {self.name}\n"
        if self.title:
            output += f"User-readable title: {self.title}\n"
        output += f"Description: {self.description}\nArguments:\n{chr(10).join(args_desc)}\n"
        return output