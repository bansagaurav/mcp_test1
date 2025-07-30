#!/usr/bin/env python3
"""
MCP Sum Server - A Simple Model Context Protocol Server

This is a basic MCP server that demonstrates how to create a server with a single tool
for adding two numbers. This file serves as the main entry point for our MCP server.

What is MCP (Model Context Protocol)?
====================================
MCP is a protocol that allows AI assistants to interact with external tools and resources
in a standardized way. It defines how servers can expose tools, resources, and prompts
that AI models can use to extend their capabilities.

Why do we need this specific file structure?
===========================================
1. This main Python file contains the server logic and tool definitions
2. We need a separate requirements.txt for dependency management
3. We need a README.md for documentation and usage instructions
4. We might need additional configuration files depending on deployment needs
"""

# Import necessary libraries for MCP server functionality
import asyncio  # For asynchronous programming - MCP servers are async by nature
import logging  # For logging server events and debugging information
from typing import Any, Sequence  # For type hints to make code more readable and maintainable

# Import MCP-specific modules
# These are the core components needed to build an MCP server
from mcp import McpError
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)

# Configure logging to help with debugging and monitoring
# This is crucial for understanding what's happening in your server
logging.basicConfig(
    level=logging.INFO,  # Set to INFO level to see important events
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output logs to console
        # You could add FileHandler here to also log to a file
    ]
)
logger = logging.getLogger(__name__)

# Create the MCP server instance
# The Server class is the main component that handles MCP protocol communication
server = Server("sum-calculator")

# Why do we need this @server.list_tools decorator?
# ==============================================
# This decorator registers a handler function that will be called when a client
# (like an AI assistant) asks "what tools are available on this server?"
# The MCP protocol requires servers to be able to list their available tools
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    Handle requests to list available tools.
    
    This function is called when a client connects and wants to know what
    tools this server provides. It must return a list of Tool objects that
    describe each available tool.
    
    Returns:
        list[Tool]: A list containing all available tools on this server
    """
    logger.info("Client requested list of available tools")
    
    # Return a list with our single tool definition
    # Each Tool object describes:
    # - name: unique identifier for the tool
    # - description: what the tool does (shown to the AI)
    # - inputSchema: JSON schema describing expected parameters
    return [
        Tool(
            name="sum_two_numbers",
            description="Calculate the sum of two numbers. This tool takes two numeric inputs and returns their mathematical sum.",
            inputSchema={
                # JSON Schema defines the structure of expected input
                # This helps both the AI and the server validate inputs
                "type": "object",  # Input should be a JSON object
                "properties": {
                    # Define each parameter the tool expects
                    "a": {
                        "type": "number",  # First number (can be integer or float)
                        "description": "The first number to add"
                    },
                    "b": {
                        "type": "number",  # Second number (can be integer or float)
                        "description": "The second number to add"
                    }
                },
                # Both parameters are required - the tool won't work without them
                "required": ["a", "b"]
            }
        )
    ]

# Why do we need this @server.call_tool decorator?
# ==============================================
# This decorator registers a handler function that will be called when a client
# wants to actually execute one of our tools. The MCP protocol separates
# "listing tools" from "calling tools" for security and clarity.
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    """
    Handle requests to execute a specific tool.
    
    This function is called when a client wants to run one of our tools.
    It receives the tool name and arguments, then executes the appropriate logic.
    
    Args:
        name (str): The name of the tool to execute
        arguments (dict): The arguments passed to the tool (can be None)
    
    Returns:
        list[TextContent]: The result of the tool execution
        
    Raises:
        McpError: If the tool name is unknown or arguments are invalid
    """
    logger.info(f"Client requested to call tool: {name} with arguments: {arguments}")
    
    # Check if the requested tool exists
    # This is important for error handling and security
    if name != "sum_two_numbers":
        logger.error(f"Unknown tool requested: {name}")
        raise McpError(f"Unknown tool: {name}")
    
    # Validate that arguments were provided
    # MCP allows arguments to be None, so we need to check
    if arguments is None:
        logger.error("No arguments provided to sum_two_numbers tool")
        raise McpError("Arguments are required for sum_two_numbers tool")
    
    # Extract the numbers from arguments with error handling
    # We need to be defensive about the input we receive
    try:
        # Get the two numbers from the arguments dictionary
        num_a = arguments.get("a")
        num_b = arguments.get("b")
        
        # Validate that both numbers were provided
        if num_a is None or num_b is None:
            raise McpError("Both 'a' and 'b' parameters are required")
        
        # Ensure the values are actually numbers
        # Python's numeric types include int, float, and complex
        if not isinstance(num_a, (int, float)) or not isinstance(num_b, (int, float)):
            raise McpError("Both 'a' and 'b' must be numbers")
        
        # Perform the actual calculation
        result = num_a + num_b
        
        logger.info(f"Successfully calculated: {num_a} + {num_b} = {result}")
        
        # Return the result as TextContent
        # MCP requires results to be wrapped in specific content types
        return [
            TextContent(
                type="text",
                text=f"The sum of {num_a} and {num_b} is {result}"
            )
        ]
        
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error calculating sum: {str(e)}")
        # Re-raise as McpError so the client gets a proper error response
        raise McpError(f"Error calculating sum: {str(e)}")

# Why do we need this main function and async setup?
# ================================================
# MCP servers are asynchronous by design because they need to handle multiple
# concurrent requests efficiently. The main function sets up the async event loop
# and starts the server using stdio (standard input/output) communication.
async def main():
    """
    Main function to start the MCP server.
    
    This function initializes and runs the MCP server using stdio transport.
    stdio transport means the server communicates through standard input/output,
    which is the most common way MCP servers are used.
    """
    logger.info("Starting MCP Sum Server...")
    
    # Why stdio_server?
    # ================
    # stdio_server is a transport method that allows the MCP server to communicate
    # through standard input and output streams. This is the most common transport
    # for MCP servers because:
    # 1. It's simple and doesn't require network configuration
    # 2. It works well with process spawning (how most MCP clients start servers)
    # 3. It's secure since it doesn't open network ports
    # 4. It's efficient for local communication
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server streams established, initializing MCP server...")
        
        # Initialize the server with the read/write streams
        # This connects our server logic to the MCP protocol transport
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="sum-calculator",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

# Standard Python idiom for script execution
# This ensures the main function only runs when the script is executed directly,
# not when it's imported as a module in another script
if __name__ == "__main__":
    """
    Entry point when the script is run directly.
    
    This block only executes when someone runs 'python mcp_sum_server.py'
    It won't execute if this file is imported as a module in another script.
    """
    logger.info("MCP Sum Server starting up...")
    
    try:
        # Run the async main function
        # asyncio.run() creates an event loop, runs the coroutine, and cleans up
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        logger.info("Server shutdown requested by user (Ctrl+C)")
    except Exception as e:
        # Handle any unexpected errors
        logger.error(f"Server encountered an unexpected error: {str(e)}")
        raise
    finally:
        logger.info("MCP Sum Server has stopped")

"""
Additional Notes for Understanding:
==================================

1. Why is this server asynchronous?
   - MCP servers need to handle multiple requests concurrently
   - Async/await allows efficient handling of I/O operations
   - It prevents the server from blocking on slow operations

2. Why do we use decorators (@server.list_tools, @server.call_tool)?
   - Decorators provide a clean way to register handler functions
   - They automatically handle MCP protocol details
   - They make the code more readable and maintainable

3. Why do we need error handling?
   - MCP clients expect proper error responses
   - Good error handling helps with debugging
   - It prevents the server from crashing on invalid input

4. Why do we use logging?
   - Helps with debugging when things go wrong
   - Provides visibility into server operations
   - Essential for production deployments

5. Why JSON Schema for input validation?
   - Standard way to describe expected data structure
   - Helps AI assistants understand how to use the tool
   - Enables automatic validation of inputs
"""