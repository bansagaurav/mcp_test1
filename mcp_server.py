#!/usr/bin/env python3
"""
Basic MCP Server Example

This server provides basic tools for file operations and text processing.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
server = Server("basic-mcp-server")


class FileReadArgs(BaseModel):
    """Arguments for read_file tool"""
    path: str


class FileWriteArgs(BaseModel):
    """Arguments for write_file tool"""
    path: str
    content: str


class TextProcessArgs(BaseModel):
    """Arguments for text processing tools"""
    text: str
    operation: Optional[str] = "uppercase"


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="read_file",
            description="Read the contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["path", "content"]
            }
        ),
        Tool(
            name="list_directory",
            description="List contents of a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the directory to list"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="text_process",
            description="Process text with various operations (uppercase, lowercase, reverse, word_count)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to process"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["uppercase", "lowercase", "reverse", "word_count"],
                        "description": "Operation to perform on the text",
                        "default": "uppercase"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="calculate",
            description="Perform basic mathematical calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')"
                    }
                },
                "required": ["expression"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any]
) -> CallToolResult:
    """Handle tool calls"""
    
    try:
        if name == "read_file":
            args = FileReadArgs(**arguments)
            try:
                content = Path(args.path).read_text()
                return CallToolResult(
                    content=[TextContent(type="text", text=content)]
                )
            except FileNotFoundError:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: File '{args.path}' not found")]
                )
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error reading file: {str(e)}")]
                )
        
        elif name == "write_file":
            args = FileWriteArgs(**arguments)
            try:
                Path(args.path).parent.mkdir(parents=True, exist_ok=True)
                Path(args.path).write_text(args.content)
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Successfully wrote to '{args.path}'")]
                )
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error writing file: {str(e)}")]
                )
        
        elif name == "list_directory":
            path = arguments.get("path", ".")
            try:
                dir_path = Path(path)
                if not dir_path.exists():
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Error: Directory '{path}' does not exist")]
                    )
                
                if not dir_path.is_dir():
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Error: '{path}' is not a directory")]
                    )
                
                items = []
                for item in sorted(dir_path.iterdir()):
                    item_type = "directory" if item.is_dir() else "file"
                    size = item.stat().st_size if item.is_file() else "-"
                    items.append(f"{item_type:9} {size:>8} {item.name}")
                
                result = f"Contents of '{path}':\n" + "\n".join(items)
                return CallToolResult(
                    content=[TextContent(type="text", text=result)]
                )
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error listing directory: {str(e)}")]
                )
        
        elif name == "text_process":
            args = TextProcessArgs(**arguments)
            operation = args.operation or "uppercase"
            
            if operation == "uppercase":
                result = args.text.upper()
            elif operation == "lowercase":
                result = args.text.lower()
            elif operation == "reverse":
                result = args.text[::-1]
            elif operation == "word_count":
                word_count = len(args.text.split())
                char_count = len(args.text)
                result = f"Words: {word_count}, Characters: {char_count}"
            else:
                result = f"Unknown operation: {operation}"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result)]
            )
        
        elif name == "calculate":
            expression = arguments.get("expression", "")
            try:
                # Simple evaluation - in production, use a safer expression evaluator
                # This is just for demonstration purposes
                allowed_chars = set("0123456789+-*/(). ")
                if not all(c in allowed_chars for c in expression):
                    return CallToolResult(
                        content=[TextContent(type="text", text="Error: Invalid characters in expression")]
                    )
                
                result = eval(expression)
                return CallToolResult(
                    content=[TextContent(type="text", text=f"{expression} = {result}")]
                )
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error calculating: {str(e)}")]
                )
        
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")]
            )
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")]
        )


async def main():
    """Run the MCP server"""
    logger.info("Starting Basic MCP Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="basic-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())