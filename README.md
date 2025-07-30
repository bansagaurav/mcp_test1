# MCP Sum Server - A Simple Model Context Protocol Server

## Why Do We Need This README.md File?

### 1. **Documentation is Critical for Software Projects**
- **User Guidance**: New users need to understand what this project does and how to use it
- **Setup Instructions**: Step-by-step guidance prevents frustration and support requests
- **Context and Purpose**: Explains the "why" behind the project, not just the "what"
- **Maintenance**: Future developers (including yourself) need to understand the codebase

### 2. **Markdown (.md) Format Benefits**
- **Universal Readability**: Displays nicely on GitHub, GitLab, and other platforms
- **Rich Formatting**: Supports headers, code blocks, links, and lists for better organization
- **Plain Text Base**: Can be read in any text editor, even without rendering
- **Standard Practice**: README.md is the expected documentation file name in software projects

### 3. **Separate File Organization**
- **Separation of Concerns**: Code files contain implementation, documentation files contain explanation
- **Easier Maintenance**: Can update documentation without touching code and vice versa
- **Better Collaboration**: Non-technical team members can contribute to documentation
- **Version Control**: Documentation changes can be tracked separately from code changes

## What This Project Does

This is a minimal MCP (Model Context Protocol) server that provides a single tool for adding two numbers. It demonstrates:

- How to create an MCP server from scratch
- How to define and register tools
- How to handle tool execution requests
- Proper error handling and logging
- Asynchronous programming patterns for MCP servers

## Project Structure

```
mcp-sum-server/
├── mcp_sum_server.py    # Main server implementation with extensive comments
├── requirements.txt     # Python dependencies with detailed explanations
└── README.md           # This documentation file
```

### Why This File Structure?

- **`mcp_sum_server.py`**: Contains the actual server logic and tool implementations
- **`requirements.txt`**: Specifies Python package dependencies for reproducible installations
- **`README.md`**: Provides documentation, setup instructions, and usage examples

## Prerequisites

Before running this MCP server, you need:

1. **Python 3.8 or higher**
   ```bash
   python --version  # Should show 3.8.0 or higher
   ```

2. **pip (Python package installer)**
   ```bash
   pip --version  # Should show pip version
   ```

3. **Virtual environment (strongly recommended)**
   - Prevents dependency conflicts with other Python projects
   - Keeps your system Python clean

## Installation and Setup

### Step 1: Clone or Download the Project
```bash
# If using git:
git clone <repository-url>
cd mcp-sum-server

# Or simply download the files to a directory
```

### Step 2: Create a Virtual Environment
```bash
# Create virtual environment
python -m venv mcp_env

# Activate it (Linux/Mac):
source mcp_env/bin/activate

# Activate it (Windows):
mcp_env\Scripts\activate

# You should see (mcp_env) in your terminal prompt
```

### Step 3: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list  # Should show mcp and its dependencies
```

## Running the Server

### Basic Usage
```bash
# Make sure your virtual environment is activated
python mcp_sum_server.py
```

The server will start and wait for MCP protocol messages on stdin/stdout.

### Testing the Server

Since this is an MCP server, it's designed to be used by MCP clients (like AI assistants). However, you can test it manually:

1. **Check Server Startup**: The server should start without errors and show log messages
2. **Integration Testing**: Use with an MCP-compatible client
3. **Manual Testing**: Send MCP protocol messages (advanced users only)

## How the Tool Works

The server provides one tool called `sum_two_numbers`:

- **Purpose**: Adds two numbers together
- **Input**: Two parameters `a` and `b` (both must be numbers)
- **Output**: Text message with the sum
- **Example**: If you pass `a=5` and `b=3`, it returns "The sum of 5 and 3 is 8"

## MCP Integration

### What is MCP?
Model Context Protocol (MCP) is a standard that allows AI assistants to interact with external tools and resources. This server can be used by:

- AI coding assistants (like Cursor, VS Code with AI extensions)
- Chat applications with tool support
- Custom MCP clients
- Development environments with MCP integration

### Connecting to MCP Clients

The exact connection method depends on your MCP client, but typically involves:

1. **Server Registration**: Tell the client about this server
2. **Process Spawning**: The client starts this Python script
3. **stdio Communication**: The client and server communicate through standard input/output
4. **Tool Discovery**: The client asks for available tools (gets our sum tool)
5. **Tool Execution**: The client can call the sum tool with parameters

## Code Architecture Explained

### Why Asynchronous Programming?
```python
async def main():
    # MCP servers use async/await because:
    # 1. Handle multiple requests concurrently
    # 2. Don't block on I/O operations
    # 3. Better performance and responsiveness
```

### Why Decorators for Tool Registration?
```python
@server.list_tools()
async def handle_list_tools():
    # Decorators provide clean separation:
    # 1. Register handlers automatically
    # 2. Handle MCP protocol details
    # 3. Keep code organized and readable
```

### Why JSON Schema for Input Validation?
```python
"inputSchema": {
    "type": "object",
    "properties": {
        "a": {"type": "number", "description": "First number"},
        "b": {"type": "number", "description": "Second number"}
    },
    "required": ["a", "b"]
}
# Benefits:
# 1. Self-documenting API
# 2. Automatic validation
# 3. AI assistants understand expected inputs
# 4. Standard format across tools
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'mcp'**
   - **Solution**: Install dependencies with `pip install -r requirements.txt`
   - **Cause**: The MCP library isn't installed

2. **Python version too old**
   - **Solution**: Upgrade to Python 3.8 or higher
   - **Cause**: MCP requires modern Python features

3. **Server starts but doesn't respond**
   - **Solution**: Ensure you're using it with an MCP client
   - **Cause**: MCP servers don't have interactive interfaces

4. **Permission denied errors**
   - **Solution**: Check file permissions, use virtual environment
   - **Cause**: System-wide Python installation restrictions

### Debugging Tips

1. **Check Logs**: The server outputs detailed logs to help diagnose issues
2. **Verify Installation**: Use `pip list` to confirm dependencies are installed
3. **Test Environment**: Try running in a fresh virtual environment
4. **Check Python Version**: Ensure compatibility with `python --version`

## Extending the Server

### Adding More Tools

To add additional tools to this server:

1. **Define the Tool**: Add it to the `handle_list_tools()` function
2. **Implement Logic**: Add handling in `handle_call_tool()`
3. **Update Documentation**: Modify this README with new tool information

Example structure for a new tool:
```python
# In handle_list_tools():
Tool(
    name="multiply_numbers",
    description="Multiply two numbers",
    inputSchema={
        "type": "object",
        "properties": {
            "x": {"type": "number", "description": "First number"},
            "y": {"type": "number", "description": "Second number"}
        },
        "required": ["x", "y"]
    }
)

# In handle_call_tool():
elif name == "multiply_numbers":
    result = arguments["x"] * arguments["y"]
    return [TextContent(type="text", text=f"Result: {result}")]
```

### Configuration Options

For production use, consider adding:
- Configuration files (JSON, YAML, or .env)
- Command-line argument parsing
- Environment variable support
- Logging configuration options

## Security Considerations

### Input Validation
- Always validate inputs before processing
- Use JSON Schema for structured validation
- Handle edge cases (None, invalid types, etc.)

### Error Handling
- Never expose internal errors to clients
- Log detailed errors for debugging
- Return user-friendly error messages

### Resource Management
- Consider rate limiting for production use
- Implement timeouts for long-running operations
- Monitor memory usage for complex tools

## Contributing

If you want to improve this server:

1. **Fork the Project**: Create your own copy
2. **Make Changes**: Add features or fix bugs
3. **Test Thoroughly**: Ensure your changes work
4. **Update Documentation**: Modify this README if needed
5. **Submit Changes**: Create a pull request

## License and Usage

This code is provided as an educational example. Feel free to:
- Use it as a starting point for your own MCP servers
- Modify it for your specific needs
- Share it with others learning MCP development

## Additional Resources

### Learning More About MCP
- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)
- [MCP Python SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)

### Python Async Programming
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Real Python Async Tutorial](https://realpython.com/async-io-python/)

### JSON Schema
- [JSON Schema Official Site](https://json-schema.org/)
- [Understanding JSON Schema](https://json-schema.org/understanding-json-schema/)

---

## Why This Level of Documentation?

You might wonder why this README is so detailed for such a simple server. Here's why comprehensive documentation matters:

1. **Learning Tool**: Helps developers understand not just "what" but "why"
2. **Reduces Support**: Answers common questions before they're asked
3. **Professional Standard**: Real-world software requires good documentation
4. **Future Reference**: You'll thank yourself later when you need to modify the code
5. **Knowledge Sharing**: Helps others learn from your work

Remember: Code is written once but read many times. Good documentation makes that reading experience much better!