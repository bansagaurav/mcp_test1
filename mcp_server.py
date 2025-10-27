#!/usr/bin/env python3
"""
Simple MCP Server - Addition Tool Only

This is a minimal Model Context Protocol (MCP) server that demonstrates
the basic structure and implementation. It provides only one tool:
adding two numbers together.

WHY THIS FILE EXISTS:
This is the main server file that implements the MCP protocol. It defines
what tools are available and how they work when called by MCP clients.

WHAT MCP IS:
MCP (Model Context Protocol) is a standardized way for AI assistants to
interact with external tools and data sources. Instead of the AI trying
to do everything itself, it can call specialized tools through MCP.

HOW THIS WORKS:
1. MCP clients (like Claude Desktop) connect to this server
2. The client asks "what tools do you have?" - we respond with our tool list
3. The client can then call our tools with specific arguments
4. We execute the tool and return results back to the client
"""

import asyncio
import logging
from typing import Any, Dict, List

# These imports are from the MCP library - each serves a specific purpose:
from mcp.server import Server  # Main server class that handles MCP protocol
from mcp.server.models import InitializationOptions  # Configuration for server startup
from mcp.server.stdio import stdio_server  # Handles communication via stdin/stdout
from mcp.types import (
    Tool,  # Defines what a tool looks like (name, description, parameters)
    CallToolResult,  # What we send back when a tool is called
    TextContent,  # Type for text responses
)
from pydantic import BaseModel  # For validating input arguments

# Set up logging so we can see what's happening when the server runs
# This helps with debugging - you'll see messages in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the main server instance with a unique name
# This name identifies our server to MCP clients
server = Server("simple-addition-server")


class AdditionArgs(BaseModel):
    """
    This class defines what arguments our addition tool expects.
    
    WHY WE USE PYDANTIC:
    Pydantic automatically validates that:
    - Both 'a' and 'b' are provided
    - Both are numbers (int or float)
    - If validation fails, it gives clear error messages
    
    This is much safer than manually checking arguments!
    """
    a: float  # First number to add
    b: float  # Second number to add


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """
    This function tells MCP clients what tools we have available.
    
    WHY THIS IS NEEDED:
    When an MCP client connects, it first asks "what can you do?"
    This function provides that answer. It's like a menu of available tools.
    
    THE TOOL DEFINITION:
    - name: How the client will refer to this tool
    - description: Human-readable explanation of what it does
    - inputSchema: JSON Schema defining what parameters the tool needs
    
    JSON Schema is a standard way to describe data structures.
    It tells the client exactly what arguments to send.
    """
    return [
        Tool(
            name="add_numbers",
            description="Add two numbers together and return the result",
            inputSchema={
                "type": "object",  # The input should be a JSON object
                "properties": {
                    "a": {
                        "type": "number",  # First parameter: a number
                        "description": "The first number to add"
                    },
                    "b": {
                        "type": "number",  # Second parameter: a number
                        "description": "The second number to add"
                    }
                },
                "required": ["a", "b"]  # Both parameters are mandatory
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """
    This function actually executes tools when the client calls them.
    
    WHEN THIS RUNS:
    After a client knows our tools (from list_tools), it can call them.
    The client sends: tool name + arguments
    We process it and send back: results
    
    PARAMETERS:
    - name: Which tool the client wants to use (e.g., "add_numbers")
    - arguments: The data the client is sending (e.g., {"a": 5, "b": 3})
    
    RETURN VALUE:
    CallToolResult containing the response we want to send back.
    """
    
    # Log what tool was called - helpful for debugging
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    try:
        # Check if the requested tool is one we actually have
        if name == "add_numbers":
            # Use Pydantic to validate and parse the arguments
            # This automatically checks that 'a' and 'b' are numbers
            args = AdditionArgs(**arguments)
            
            # Perform the actual addition
            result = args.a + args.b
            
            # Log the calculation for debugging
            logger.info(f"Calculated: {args.a} + {args.b} = {result}")
            
            # Return the result wrapped in the required MCP format
            return CallToolResult(
                content=[
                    TextContent(
                        type="text", 
                        text=f"The sum of {args.a} and {args.b} is {result}"
                    )
                ]
            )
        
        else:
            # If someone asks for a tool we don't have, tell them
            return CallToolResult(
                content=[
                    TextContent(
                        type="text", 
                        text=f"Unknown tool: {name}. I only know how to add_numbers."
                    )
                ]
            )
    
    except Exception as e:
        # If anything goes wrong, return a helpful error message
        # This could happen if arguments are missing or wrong type
        logger.error(f"Error in tool {name}: {str(e)}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text", 
                    text=f"Error: {str(e)}"
                )
            ]
        )


async def main():
    """
    This is the main function that starts and runs the MCP server.
    
    HOW MCP COMMUNICATION WORKS:
    MCP servers communicate through stdin/stdout (standard input/output).
    This means:
    - The client sends JSON messages through stdin
    - We send JSON responses through stdout
    - This works across different programming languages and systems
    
    WHY ASYNC:
    We use async/await because MCP servers need to handle multiple
    requests efficiently without blocking. This is especially important
    for servers that might do file I/O, network requests, or other
    potentially slow operations.
    """
    logger.info("Starting Simple Addition MCP Server...")
    logger.info("This server provides one tool: add_numbers")
    logger.info("Connect an MCP client to start using it!")
    
    # Set up stdin/stdout communication
    async with stdio_server() as (read_stream, write_stream):
        # Run the server with our configuration
        await server.run(
            read_stream,  # Where we read client messages from
            write_stream,  # Where we send responses to
            InitializationOptions(
                server_name="simple-addition-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


# This is Python's standard way to run code when the file is executed directly
# (as opposed to being imported as a module)
if __name__ == "__main__":
    """
    WHY WE USE asyncio.run():
    Since our main() function is async, we need asyncio.run() to start
    the event loop and run our async code. This is the entry point that
    begins everything.
    """
    asyncio.run(main())