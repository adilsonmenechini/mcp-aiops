import asyncio
import logging
import os
import shutil
from contextlib import AsyncExitStack
from typing import Any, List
from mcp import ClientSession,StdioServerParameters, Tool as McpTool
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client


class Server:
    """
    Manages the connection to a single Model Context Protocol (MCP) server.
    Handles server initialization, listing available tools, executing tools,
    and proper cleanup of resources.
    Supports both 'stdio' (local process) and 'sse' (network) transports.
    """
    def __init__(self, name: str, config: dict[str, Any]) -> None:
        self.name: str = name
        self.config: dict[str, Any] = config
        self.session: ClientSession | None = None
        self._cleanup_lock: asyncio.Lock = asyncio.Lock()
        self.exit_stack: AsyncExitStack = AsyncExitStack()

    async def initialize(self) -> None:
        """
        Initializes the connection to the MCP server based on its configuration.
        Correctly handles both 'stdio' and 'sse' transports based on the provided JSON.
        """
        transport_type = self.config.get("transport", "stdio").lower()
        transport_context_manager: Any = None

        try:
            if transport_type == "stdio":
                command_name = self.config.get("command")
                if not command_name:
                    raise ValueError(f"A 'command' must be specified for stdio transport on server '{self.name}'.")

                command_path = shutil.which(command_name)
                if command_path is None:
                    raise ValueError(f"The command '{command_name}' for server '{self.name}' was not found in the system's PATH.")

                args = self.config.get("args", [])
                env = self.config.get("env")
                full_env = {**os.environ, **env} if env else os.environ
                
                server_params = StdioServerParameters(
                    command=command_path,
                    args=args,
                    env=full_env,
                )
                logging.info(f"Initializing server '{self.name}' with stdio command: {command_path} {' '.join(args)}")
                transport_context_manager = stdio_client(server_params)

            elif transport_type == "sse":
                url = self.config.get("url")
                if not url:
                    raise ValueError(f"A 'url' must be specified for sse transport on server '{self.name}'.")

                logging.info(f"Initializing server '{self.name}' with SSE transport at URL: {url}")
                
                transport_context_manager = sse_client(
                    url=url,
                    headers=self.config.get("headers"),
                    sse_read_timeout=self.config.get("sse_read_timeout", 900), # <-- Nome do argumento corrigido para corresponder à função
                )

            
            else:
                raise ValueError(f"Unsupported MCP transport type for server '{self.name}': {transport_type}")

            transport = await self.exit_stack.enter_async_context(transport_context_manager)
            read, write = transport
            
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            
            self.session = session
            logging.info(f"Server {self.name} initialized successfully.")

        except Exception as e:
            logging.error(f"Error initializing server {self.name}: {e}")
            await self.cleanup()
            raise

    async def list_tools(self) -> list['Tool']:
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        logging.info(f"Listing tools for server {self.name}...")
        tools_response = await self.session.list_tools()
        tools = []

        for item in tools_response:
            if isinstance(item, tuple) and item[0] == "tools" and isinstance(item[1], list):
                mcp_tools: List[McpTool] = item[1]
                tools.extend(
                    Tool(tool.name, tool.description, tool.inputSchema, getattr(tool, 'title', None))
                    for tool in mcp_tools
                )
        logging.info(f"Found {len(tools)} tools on server {self.name}.")
        return tools

    async def execute_tool(self, tool_name: str, arguments: dict[str, Any], retries: int = 2, delay: float = 1.0) -> Any:
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        attempt = 0
        while attempt < retries:
            try:
                logging.info(f"Attempting to execute tool '{tool_name}' on server {self.name} (Attempt {attempt + 1}/{retries})")
                logging.debug(f"Arguments for '{tool_name}': {arguments}") 

                result = await self.session.call_tool(tool_name, arguments)
                logging.debug(f"Raw result from tool '{tool_name}': {result}")

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
                    raise

    async def cleanup(self) -> None:
        async with self._cleanup_lock:
            if self.session:
                logging.info(f"Cleaning up server {self.name}...")
            try:
                await self.exit_stack.aclose()
                self.session = None
                logging.info(f"Server {self.name} cleaned up.")
            except Exception as e:
                logging.error(f"Error during cleanup of server {self.name}: {e}")


class Tool:
    def __init__(self, name: str, description: str, input_schema: dict[str, Any], title: str | None = None) -> None:
        self.name: str = name
        self.title: str | None = title
        self.description: str = description
        self.input_schema: dict[str, Any] = input_schema

    def format_for_llm(self) -> str:
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
        output += f"Description: {self.description}\n"
        if args_desc:
            output += f"Arguments:\n{chr(10).join(args_desc)}\n"
        else:
            output += "Arguments: None\n"
        return output